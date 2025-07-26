set number
set relativenumber
set tabstop=4
set shiftwidth=4
" nnoremap j k
" nnoremap k j
set mouse=a
set spell
set spelllang=en
set termguicolors

" word autocorrection setup
xnoremap <leader>s :<C-u>call SpellCorrectVisual()<CR>

" telescope key bindings
nnoremap <leader>ff :Telescope find_files<CR>
nnoremap <leader>fg :Telescope live_grep<CR> 

function! SpellCorrectVisual()
  " Get the selected word
  let l:word = getline("'<")[getpos("'<")[2] - 1 : getpos("'>")[2] - 1]
  call setpos('.', getpos("'<"))
  " Show spelling suggestions
  let l:suggestions = spellsuggest(l:word)
  if !empty(l:suggestions)
    echo "Suggestions:"
    for i in range(len(l:suggestions))
      echo (i + 1) . '. ' . l:suggestions[i]
    endfor
    let l:choice = input("Choose correction (0 to cancel): ")
    if l:choice =~ '^\d\+$' && l:choice > 0 && l:choice <= len(l:suggestions)
      execute "normal! gv\"_c" . l:suggestions[l:choice - 1]
    endif
  else
    echo "No suggestions."
  endif
endfunction


call plug#begin('~/.local/share/nvim/plugged')

Plug 'neovim/nvim-lspconfig'
Plug 'hrsh7th/nvim-cmp'
Plug 'hrsh7th/cmp-nvim-lsp'
Plug 'L3MON4D3/LuaSnip'
Plug 'saadparwaiz1/cmp_luasnip'
Plug 'windwp/nvim-autopairs'
Plug 'hrsh7th/cmp-buffer'
Plug 'numToStr/Comment.nvim'
Plug 'nvim-tree/nvim-tree.lua'
" Plug 'nvim-telescope/telescope.nvim'
" Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-lualine/lualine.nvim'
Plug 'lukas-reineke/indent-blankline.nvim'
Plug 'j-hui/fidget.nvim'
Plug 'lewis6991/gitsigns.nvim'
Plug 'morhetz/gruvbox'
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-telescope/telescope.nvim'
Plug 'norcalli/nvim-colorizer.lua'

call plug#end()

" comment using ctrl+/ setup
nmap <silent> <C-_> <Plug>(comment_toggle_linewise)
xmap <silent> <C-_> <Plug>(comment_toggle_linewise_visual)


" python colorscheme
colorscheme gruvbox

lua << EOF
-- python lsp setup
require('lspconfig').pyright.setup{}

-- autocomplete setup
local cmp = require('cmp')
local luasnip = require('luasnip')

cmp.setup({
  snippet = {
    expand = function(args)
      luasnip.lsp_expand(args.body)
    end,
  },
  sources = {
    { name = 'nvim_lsp' },
    { name = 'luasnip' },
	{ name = 'buffer' },
	{ name = 'spell' },
  },
  mapping = {
    ['<S-Tab>'] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Insert }),
    ['<Tab>'] = cmp.mapping.confirm({ select = true }),
  }
})

-- autopairing setup
require('nvim-autopairs').setup{}

-- commenting setup
require('Comment').setup({
  toggler = {
    line = '<C-_>',    -- your Ctrl+/ mapping for line comments
    block = nil,       -- disable block comment toggler completely
  },
  opleader = {
    line = '<C-_>',    -- line comment operator for visual mode
    block = nil,       -- disable block comment operator
  },
  pre_hook = nil,      -- no pre-hook needed
})

-- file explorer(sidebar) setup, ctrl+n
require("nvim-tree").setup()
vim.keymap.set('n', '<C-n>', ':NvimTreeToggle<CR>')

-- status line setup
require("lualine").setup()

-- indent lines setup
require("ibl").setup()

-- lsp ui setup
require("fidget").setup({})

-- git indicators
require("gitsigns").setup()

-- colored hex
require("colorizer").setup()
EOF
