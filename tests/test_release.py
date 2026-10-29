import importlib.util, unittest
from pathlib import Path
from tempfile import TemporaryDirectory

root = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, root / 'scripts' / f'{name}.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


deploy = module('deploy')
edge_rules = module('edge_rules')
indexnow = module('indexnow')
mcp_script = module('mcp_script')


class Release(unittest.TestCase):
    def test_assets_upload_before_documents_and_manifest_last(self):
        with TemporaryDirectory() as directory:
            r = Path(directory)
            for name in ['index.html', 'catalog.json', 'index.xml', 'main.123.css', 'image.webp', 'index.md', 'release-manifest.json']:
                (r / name).write_text('fixture')
            order = [p.name for p in deploy.upload_order(r)]
            self.assertLess(order.index('main.123.css'), order.index('index.html'))
            self.assertLess(order.index('image.webp'), order.index('index.html'))
            self.assertLess(order.index('index.md'), order.index('catalog.json'))
            self.assertEqual(order[-1], 'release-manifest.json')

    def test_indexnow_submits_only_changed_entries(self):
        before = {'items': [{'id': 'one', 'content_hash': 'old'}]}
        current = {'items': [{'id': 'one', 'content_hash': 'old', 'canonical_url': 'https://example.test/one/'},
                             {'id': 'two', 'content_hash': 'new', 'canonical_url': 'https://example.test/two/'}]}
        self.assertEqual(indexnow.changed_urls(before, current), ['https://example.test/two/'])

    def test_mime_types_for_agent_files(self):
        self.assertEqual(deploy.mime(Path('index.md')), 'text/markdown; charset=utf-8')
        self.assertEqual(deploy.mime(Path('.well-known/api-catalog')), 'application/linkset+json')
        self.assertEqual(deploy.mime(Path('feed.json')), 'application/feed+json; charset=utf-8')


    def test_edge_rules_group_redirects_by_target_within_bunny_limits(self):
        config = {'host': 'example.test', 'managedPrefix': '[repo] ', 'maxRules': 50,
                  'headers': {'X-Content-Type-Options': 'nosniff'},
                  'csp': {'header': 'Content-Security-Policy-Report-Only', 'directives': {'default-src': "'self'"}},
                  'cache': [{'name': 'Images', 'browser': 'public, max-age=86400', 'edge': 86400,
                             'patterns': ['*.webp'], 'exclude': ['*_hu_*']}],
                  'mime': [], 'canonicalFrom': ['example.test.invalid']}
        redirects = [{'from': f'/tags/t{i}/', 'to': '/topics/a/', 'status': 301} for i in range(30)]
        redirects.append({'from': '/1/', 'to': '/', 'status': 301})
        rules = edge_rules.build(config, redirects)
        to_a = [r for r in rules if r['ActionParameter1'] == 'https://example.test/topics/a/']
        self.assertEqual([r['Description'] for r in to_a], ['[repo] Redirect to /topics/a/ (1/2)', '[repo] Redirect to /topics/a/ (2/2)'])
        for r in rules:
            self.assertLessEqual(len(r['Triggers']), 5)
            self.assertTrue(all(len(t['PatternMatches']) <= 5 for t in r['Triggers']))
        root = next(r for r in rules if r['Description'] == '[repo] Redirect to /')
        self.assertEqual(root['Triggers'][0]['PatternMatches'], ['*://example.test/1/'])
        slash = next(r for r in rules if r['Description'] == '[repo] Directory URL: trailing slash')
        self.assertEqual(slash['ActionParameter1'], 'https://example.test%{Url.Directory}%{Url.FileName}/')
        self.assertEqual([t['Type'] for t in slash['Triggers']], [0, 3, 6])
        self.assertIn('*://example.test/.well-known*', slash['Triggers'][0]['PatternMatches'])
        images = next(r for r in rules if r['Description'] == '[repo] Cache: Images')
        self.assertEqual((images['TriggerMatchingType'], images['Triggers'][1]['PatternMatchingType']), (1, 2))
        config['cache'].append({'name': 'Documents', 'browserTtl': 0, 'edge': 300, 'patterns': ['*/']})
        documents = next(r for r in edge_rules.build(config, redirects) if r['Description'] == '[repo] Cache: Documents')
        self.assertEqual((documents['ActionType'], documents['ActionParameter1']), (16, '0'))
        self.assertEqual(documents['ExtraActions'][0]['ActionParameter1'], '300')
        config['cache'].pop()
        headers = rules[0]
        self.assertEqual(headers['ExtraActions'][0]['ActionParameter1'], 'Content-Security-Policy-Report-Only')
        config['maxRules'] = 3
        with self.assertRaises(SystemExit):
            edge_rules.build(config, redirects)

    def test_edge_rules_compare_like_the_api_echoes_them(self):
        ours = edge_rules.url_rule('[repo] x', edge_rules.action(5, 'A', 'b'), ['*'])
        echoed = {**ours, 'Guid': 'g', 'OrderIndex': 3, 'ActionParameter3': '', 'ExtraActions': None,
                  'Triggers': [{**ours['Triggers'][0], 'Parameter1': ''}]}
        self.assertEqual(edge_rules.comparable(ours), edge_rules.comparable(echoed))
        self.assertNotEqual(edge_rules.comparable(ours), edge_rules.comparable({**echoed, 'ActionParameter2': 'c'}))

    def test_mcp_bundle_is_one_file_with_only_url_imports(self):
        code = mcp_script.bundle()
        imports = [line for line in code.splitlines() if line.startswith('import ')]
        self.assertTrue(imports and all('from "https://' in line for line in imports))
        self.assertNotIn('from "./', code)
        self.assertIn('export async function handle(', code)
        self.assertIn('BunnySDK.net.http.serve(', code)

    def test_mcp_registry_entry_matches_the_server_and_the_catalog(self):
        import json, re
        server = json.loads((root / 'edge/mcp/server.json').read_text())
        handler = (root / 'edge/mcp/handler.ts').read_text()
        self.assertEqual(server['version'], re.search(r'SERVER_INFO = \{[^}]*version: "([^"]+)"', handler).group(1))
        self.assertLessEqual(len(server['description']), 100)
        catalog = (root / 'static/.well-known/api-catalog').read_text()
        for remote in server['remotes']:
            self.assertIn(f'"href": "{remote["url"]}"', catalog)

    def test_capabilities_list_every_mcp_tool_at_the_server_version(self):
        import json, re
        handler = (root / 'edge/mcp/handler.ts').read_text()
        version = re.search(r'SERVER_INFO = \{[^}]*version: "([^"]+)"', handler).group(1)
        tools = re.findall(r'^    name: "([a-z_]+)",', handler, re.M)
        self.assertTrue(tools)
        listed = (root / 'static/capabilities.txt').read_text()
        structured = json.loads((root / 'static/.well-known/capabilities.json').read_text())['capabilities']
        mcp = {c['invocation']['tool']: c for c in structured if c['invocation']['type'] == 'mcp'}
        self.assertEqual(set(mcp), set(tools))
        for tool in tools:
            self.assertIn(f'- site.mcp.{tool} (v{version}) — ', listed)
            self.assertEqual((mcp[tool]['id'], mcp[tool]['version']), (f'site.mcp.{tool}', version))
            self.assertEqual(mcp[tool]['invocation']['endpoint'], json.loads((root / 'edge/mcp/server.json').read_text())['remotes'][0]['url'])

    def test_mcp_deploy_refuses_a_malformed_script_id(self):
        with self.assertRaises(SystemExit):
            mcp_script.deploy('code', '12/../34', 'key')


if __name__ == '__main__':
    unittest.main()
