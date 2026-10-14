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
indexnow = module('indexnow')


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


if __name__ == '__main__':
    unittest.main()
