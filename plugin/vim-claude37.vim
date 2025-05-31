if exists('g:loaded_vim_claude37') || &cp || v:version < 700
  finish
endif
let g:loaded_vim_claude37 = 1

if !has('python3')
    echoerr "vim-claude37 requires Vim compiled with +python3"
    finish
endif

" Default typing animation speed (milliseconds per character)
if !exists('g:claude37_typing_speed')
    let g:claude37_typing_speed = 10
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
import time

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import claude37

def animated_typing(text):
    """Add text with typing animation"""
    if not vim.eval('&modifiable') == '1':
        print("Buffer is not modifiable!")
        return
        
    delay = float(vim.eval('g:claude37_typing_speed')) / 1000.0
    current_line = vim.current.line
    row, col = vim.current.window.cursor
    
    for char in text:
        if char == '\n':
            # For newlines, append a new line and move cursor there
            vim.current.buffer.append('', row)
            row += 1
            vim.current.window.cursor = (row, 0)
            current_line = ''
            col = 0
        else:
            # Insert character at current position
            new_line = current_line[:col] + char + current_line[col:]
            vim.current.buffer[row-1] = new_line
            current_line = new_line
            col += 1
            vim.current.window.cursor = (row, col)
        
        vim.command('redraw')
        time.sleep(delay)
EOF

" Define Vim commands
command! -nargs=0 Claude37Assist py3 claude37.vim_claude37_assist()
command! -nargs=0 Claude37Clear py3 claude37.clear_buffer()

" Define key mappings
nnoremap <leader>cg :Claude37Assist<CR>
