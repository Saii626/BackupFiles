call plug#begin(stdpath('data') . '/plugged')

" Start screen
Plug 'mhinz/vim-startify'

" Coc
Plug 'neoclide/coc.nvim', {'branch': 'release'}

" rg
Plug 'jremmen/vim-ripgrep'

" systax for .log files
Plug 'dzeban/vim-log-syntax'

" NERDTree 
Plug 'preservim/nerdtree'
Plug 'Xuyuanp/nerdtree-git-plugin'

" vim
Plug 'tpope/vim-fugitive'

" quick-scope
Plug 'unblevable/quick-scope'

" arduino support
Plug 'stevearc/vim-arduino'

" platformIO support
Plug 'coddingtonbear/neomake-platformio'

call plug#end()


