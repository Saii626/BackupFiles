" set termguicolors
set t_Co=256
set number
set nocompatible
syntax enable

set path+=**
set wildmenu

set scrolloff=5
set noet
set list

set hidden
let mapleader=" "

let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
set background=dark
colorscheme gruvbox
hi! Normal ctermbg=NONE guibg=NONE

au BufNewFile,BufRead /*.rasi setf css
au BufNewFile,BufRead *.mon set filetype=epl
au BufNewFile,BufRead *.evt set filetype=epl

source ~/.config/nvim/load_plugins.vim
source ~/.config/nvim/nerd_tree.vim
source ~/.config/nvim/coc_nvim.vim
source ~/.config/nvim/nav_tabs_win.vim
source ~/.config/nvim/quick_scope.vim

" Clear highlighting on escape in normal mode
nnoremap <esc> :noh<return><esc>
nnoremap <esc>^[ <esc>^[

" terminal
nnoremap <leader>t :bel split<CR> :res 10<CR> :terminal<CR>

" Rg search from the location where the project was opened
let g:rg_derive_root=1

" quickly change configuration on the fly
nmap <leader>c :tabedit ~/.config/nvim/init.vim<CR>

" Faster movements
nmap <c-up> :z^10<CR><CR>
nmap <c-k> :z^10<CR><CR>
nmap <c-down> :z+10<CR><CR>
nmap <c-j> :z+10<CR><CR>

" Substitute the word under cursor
nmap <leader>s :%s/\<<C-r><C-w>\>//g<Left><Left>

