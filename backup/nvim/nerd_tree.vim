" Show hidden files
let NERDTreeShowHidden=1

" Mirror an already existing NERDTree instance or create a new one
function! ToggleNERDTree()
	if exists("g.NERDTree") && g.NERDTree.IsOpen()
		NERDTreeMirror
	else
		NERDTreeToggle
	endif
endfunction
nnoremap <leader>e :call ToggleNERDTree()<CR>


