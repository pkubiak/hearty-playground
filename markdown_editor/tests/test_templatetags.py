import unittest
from textwrap import dedent

from bs4 import BeautifulSoup

from ..templatetags.markdown import markdown


class ParseHTMLMixin:
    def parse_markdown_to_html(self, text):
        html = markdown(dedent(text))
        return BeautifulSoup(html, 'html5lib')

    def assertLength(self, collection, length):
        self.assertEqual(len(collection), length)


class MarkdownTemplateTagTestCase(unittest.TestCase, ParseHTMLMixin):
    def test_heading_rendering(self):
        output = markdown('# Heading #')
        self.assertEqual(output, '<h1>Heading</h1>')

    def test_tasklists(self):
        doc = self.parse_markdown_to_html("""
        - [X] Done
        - [ ] Not done
            - [ ] Nested        
        """)  # noqa

        self.assertLength(doc.select('input[type=checkbox]'), 3)
        self.assertLength(doc.select('ul.task-list'), 2)

    def test_subscript(self):
        output = markdown('CH~3~CH~2~OH')

        self.assertEqual(output, '<p>CH<sub>3</sub>CH<sub>2</sub>OH</p>')

    def test_smartsymbols(self):
        output = markdown('(tm) (c) +/- -->')

        self.assertEqual(output, '<p>™ © ± →</p>')

    def test_autolinking_link(self):
        output = markdown("https://google.com")

        self.assertEqual(output, '<p><a href="https://google.com">https://google.com</a></p>')

    def test_autolinking_email(self):
        output = markdown("fake.email@email.com")

        self.assertEqual(output, '<p><a href="mailto:fake.email@email.com">fake.email@email.com</a></p>')

    def test_supscript(self):
        output = markdown('H^2^0')

        self.assertEqual(output, '<p>H<sup>2</sup>0</p>')

    def test_emoji(self):
        doc = self.parse_markdown_to_html(':smile:')

        self.assertLength(doc.select('img'), 1)

    def test_emoji_unsupported(self):
        output = markdown(':crush:')

        self.assertEqual(output, '<p>:crush:</p>')


class MarkdownTemplateTagBootstrapPostprocessingTestCase(unittest.TestCase, ParseHTMLMixin):
    """We test that all bootstrap classes are correctly assigned."""
    def test_table(self):
        doc = self.parse_markdown_to_html("""
        | a | b |
        |---|---|
        | c | d |
        """)

        self.assertLength(doc.select('table'), 1)
        self.assertLength(doc.select('table.table'), 1)

        self.assertLength(doc.select('thead.thead-light'), 1)

        self.assertLength(doc.find_all('th'), 2)
        self.assertLength(doc.find_all('td'), 2)

    def test_alerts_without_title(self):
        doc = self.parse_markdown_to_html("""
        !!! warning ""
            This is an admonition box without a title.
        """)

        self.assertLength(doc.select('div.alert.alert-warning'), 1)

    def test_code_block_with_linenumbers(self):
        doc = self.parse_markdown_to_html("""
        ```js linenums="1"
        for(let i=0;i<5;i++);
        ```
        """)

        self.assertEqual(doc.find('table')['class'], ['highlighttable'])
