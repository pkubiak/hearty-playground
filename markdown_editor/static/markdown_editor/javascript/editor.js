class MarkdownEditor {
  constructor(element_id, config) {
    this.config = config || {};

    if('url' in this.config) {
      this.config.toolbar = this.config.toolbar || MarkdownEditor.DEFAULT_TOOLBAR;
      this.el = document.getElementById(element_id);

      this._create_container();
      this._create_hidden_form();
      this.render_markdown();
    } else
      console.warn('You must provide `url` to setup MarkdownEditor!');
  }

  onkeypress(event) {
    if(event.key == 'Enter' && event.ctrlKey)
      this.render_markdown();

    if(event.key == 'x' && event.ctrlKey)
      console.warn('Line cutting is not yet supported'); // TODO: implement line cutting: pkubiak/hearty-playground#5
  }

  render_markdown() {
    this.form.elements['text'].value = this.el.value;
    this.form.submit();
  }

  _create_hidden_form() {
    const form = document.createElement('form');
    form.action = this.config.url;
    form.method = 'POST';
    form.target = this.el.id + '_preview_iframe';

    const input = document.createElement('input');
    input.name = 'text';
    input.type = 'hidden';

    const csrf = document.createElement('input');
    csrf.name = 'csrfmiddlewaretoken';
    csrf.type = 'hidden';
    csrf.value = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    form.appendChild(input);
    form.appendChild(csrf);

    this.form = form;

    document.body.appendChild(form);
  }

  _create_container(el) {
    const that = this;
    const editor = document.createElement('div');
    editor.className = 'markdown_editor';

    const toolbar = document.createElement('nav');
    toolbar.role = 'toolbar';

    this._create_toolbar(toolbar);
    editor.appendChild(toolbar);

    const view = document.createElement('div');
    view.className = 'view';
    editor.appendChild(view);

    const iframe = document.createElement('iframe');
    iframe.name = this.el.id + '_preview_iframe';
    iframe.sandbox = 'allow-same-origin';

    iframe.addEventListener('load', function(event) {
      /* NOTE: value 150px is from HTML documentation as default height of iframe */
      that.el.style.minHeight = iframe.style.minHeight = Math.max(150, iframe.contentWindow.document.documentElement.offsetHeight) + 'px';
    });

    this.el.parentNode.insertBefore(editor, this.el);
    view.appendChild(this.el);
    view.appendChild(iframe);

    // listen for keypress to handle special keys (ctrl+enter / ctrl+x / etc.)
    this.el.addEventListener('keydown', function(event) {
      that.onkeypress(event);
    });
  }

  _create_toolbar(nav_el) {
    for(let item_name of this.config.toolbar) {
      if(item_name in MarkdownEditor.TOOLBAR_ITEMS) {
        const item = MarkdownEditor.TOOLBAR_ITEMS[item_name];

        if(item.html) {
          nav_el.insertAdjacentHTML('beforeend', item.html);
        } else
        if(item.button) {
          const el = document.createElement('button');
          el.type = 'button';
          el.innerHTML = item.button;

          if(item.action)
            el.addEventListener('click', item.action.bind(this));
          else
            el.disabled = 'disabled';

          if(item.title)
            el.title = item.title;

          nav_el.appendChild(el);
        } else {
          console.warn('Unproper definition of toolbar item: ', item_name);
        }
      } else {
        console.warn('Unsupported toolbar item:', item_name);
      }
    }
  }
}

/* ------------------------------------------------------------------------------------------------------------ */

function insert_markdown(before, placeholder, after) {
  // NOTE: based on https://www.everythingfrontend.com/posts/insert-text-into-textarea-at-cursor-position.html
  return function(event) {
    const input = this.el; // function is bind to instance of MarkdownEditor

    // make sure we have focus in the right input
    input.focus();

    // get selected text
    const start = input.selectionStart, end = input.selectionEnd;
    const selection = input.value.slice(start, end);

    // and just run the command
    const textToInsert = before + (selection || placeholder) + after;
    const isSupported =  document.execCommand('insertText', false /*no UI*/, textToInsert);

    // slower fallback for browsers which doesn't support 'insertText'
    if(!isSupported) {
      input.value = input.value.slice(0, start) + textToInsert + input.value.slice(end);
      input.selectionStart = input.selectionEnd = start + textToInsert.length;
    }

    event.preventDefault();
  }
}

function _heading_helper(nth) {
  const pattern = '#'.repeat(nth);

  return {
    'title': 'insert heading ' + nth,
    'button': '<i class="fas fa-fw fa-heading"></i>' + nth,
    'action': insert_markdown('\n' + pattern + ' ', 'heading ' + nth, ' ' + pattern + '\n')
  }
}


MarkdownEditor.TOOLBAR_ITEMS = {
  'h1': _heading_helper(1),
  'h2': _heading_helper(2),
  'h3': _heading_helper(3),
  'h4': _heading_helper(4),
  'h5': _heading_helper(5),
  'h6': _heading_helper(6),
  'image': {
    'title': 'insert image',
    'button': '<i class="far fa-fw fa-file-image"></i>',
    'action': insert_markdown('\n![alt text](', 'https://picsum.photos/300/200', ')\n')
  },
  'link': {
    'title': 'insert link',
    'button': '<i class="fas fa-fw fa-link"></i>',
    'action': insert_markdown('\n[link title](', 'url', ')\n'),
  },
  'bold': {
    'title': 'bold text',
    'button': '<i class="fas fa-fw fa-bold"></i>',
    'action': insert_markdown('**', 'text', '**')
  },
  'italic': {
    'title': 'italic text',
    'button': '<i class="fas fa-fw fa-italic"></i>',
    'action': insert_markdown('*', 'text', '*')
  },
  'mark': {
    'title': 'highlight text',
    'button': '<i class="fas fa-fw fa-highlighter"></i>',
    'action': insert_markdown('==', 'mark', '==')
  },
  'strikethrough': {
    'title': 'strikethrough text',
    'button': '<i class="fas fa-fw fa-strikethrough"></i>',
    'action': insert_markdown('~~', 'text', '~~'),
  },
  'sup': {
    'title': 'superscript text',
    'button': '<i class="fas fa-superscript"></i>',
    'action': insert_markdown('^', 'text', '^'),
  },
  'sub': {
    'title': 'subscript text',
    'button': '<i class="fas fa-subscript"></i>',
    'action': insert_markdown('~', 'text', '~'),
  },
  'ul': {
    'title': 'add unordered list',
    'button': '<i class="fas fa-fw fa-list"></i>',
    'action': insert_markdown('\n- ', 'item 1', '\n- item 2\n- item 3\n\n'),
  },
  'ol': {
    'title': 'add ordered list',
    'button': '<i class="fas fa-fw fa-list-ol"></i>',
    'action': insert_markdown('\n1. ', 'item 1', '\n2. item 2\n3. item 3\n\n'),
  },
  'task': {
    'title': 'add task list',
    'button': '<i class="fas fa-fw fa-tasks"></i>',
    'action': insert_markdown('\n- [X] ', 'task 1', '\n- [ ] task 2\n- [ ] task 3\n\n'),
  },
  'table': {
    'title': 'insert table',
    'button': '<i class="fas fa-fw fa-table"></i>',
    'action': insert_markdown('\n| column 1 | column 2 |\n|----------|----------|\n| ', 'value 1', '  | value 2  |\n\n'),
  },
  'refresh': {
    'title': 'refresh preview',
    'button': '<i class="fas fa-sync-alt"></i> Refresh preview</a>',
    'action': function(event) {this.render_markdown();},
  },
  'expand': { // TODO: implement switching between shrinked/expanded views: pkubiak/hearty-playground#3
    'title': 'expand view',
    'button': '<i class="fas fa-arrows-alt-v"></i>&nbsp;Expand'
  },
  'help': { // TODO: add help window: pkubiak/hearty-playground#4
    'title': 'show help',
    'button': '<i class="far fa-life-ring"></i>&nbsp;Help',
  },

  //-----------
  '|': {
    'html': '<span class="spacer"></span>'
  },
  '<->': {
    'html': '<span class="expander"></span>'
  }
}


MarkdownEditor.DEFAULT_TOOLBAR = [
  'h1', 'h2', 'h3', 'h4', 'h5','h6', '|',
  'image', 'link', '|',
  'bold', 'italic', 'mark', 'strikethrough', 'sup', 'sub', '|',
  'ul', 'ol', 'task', '|',
  'table', '|',
  '<->', 'refresh', 'expand', 'help'
];
