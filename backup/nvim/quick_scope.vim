augroup qs_colors
  autocmd!
  autocmd ColorScheme * highlight QuickScopePrimary guifg='#afff5f' gui=underline ctermfg=155 cterm=underline
  autocmd ColorScheme * highlight QuickScopeSecondary guifg='#5fffff' gui=underline ctermfg=81 cterm=underline
augroup END

" turn this off when line is too long
let g:qs_max_chars=100

" toggel this on/off
nmap <leader>q <plug>(QuickScopeToggle)
xmap <leader>q <plug>(QuickScopeToggle)

" Don't run this on terminal or unnamed buffer
let g:qs_buftype_blacklist = ['terminal', 'nofile']

" Wait before highlighting
let g:qs_lazy_highlight = 1
