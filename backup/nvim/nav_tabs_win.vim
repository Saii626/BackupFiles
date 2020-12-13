" Use escape to switch to normal mode in terminal
tnoremap <esc> <C-\><C-n>

" Use ALT+{h,j,k,l} to navigate windows
tnoremap <M-h> <C-\><C-N><C-w>h
inoremap <M-h> <C-\><C-N><C-w>h
nnoremap <M-h> <C-w>h
tnoremap <M-LEFT> <C-\><C-N><C-w>h
inoremap <M-LEFT> <C-\><C-N><C-w>h
nnoremap <M-LEFT> <C-w>h

tnoremap <M-j> <C-\><C-N><C-w>j
inoremap <M-j> <C-\><C-N><C-w>j
nnoremap <M-j> <C-w>j
tnoremap <M-Down> <C-\><C-N><C-w>j
inoremap <M-DOWN> <C-\><C-N><C-w>j
nnoremap <M-DOWN> <C-w>j

tnoremap <M-k> <C-\><C-N><C-w>k
inoremap <M-k> <C-\><C-N><C-w>k
nnoremap <M-k> <C-w>k
tnoremap <M-UP> <C-\><C-N><C-w>k
inoremap <M-UP> <C-\><C-N><C-w>k
nnoremap <M-UP> <C-w>k

tnoremap <M-l> <C-\><C-N><C-w>l
inoremap <M-l> <C-\><C-N><C-w>l
nnoremap <M-l> <C-w>l
tnoremap <M-RIGHT> <C-\><C-N><C-w>l
inoremap <M-RIGHT> <C-\><C-N><C-w>l
nnoremap <M-RIGHT> <C-w>l

" tabs shortcut
nnoremap <C-Left> :tabprevious<CR>
nnoremap <C-h> :tabprevious<CR>

nnoremap <C-Right> :tabnext<CR>
nnoremap <C-l> :tabnext<CR>

nnoremap <silent> <C-S-Left> :execute 'silent! tabmove ' . (tabpagenr()-2)<CR>
" nnoremap <silent> <C-S-h> :execute 'silent! tabmove ' . (tabpagenr()-2)<CR>

nnoremap <silent> <C-S-Right> :execute 'silent! tabmove ' . (tabpagenr()+1)<CR>
" nnoremap <silent> <C-S-l> :execute 'silent! tabmove ' . (tabpagenr()+1)<CR>
