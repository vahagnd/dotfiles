#
# ~/.bashrc
#

# ===== nvim is here =====
export PATH="$HOME/.local/bin:$PATH"
#
# opencode
export PATH=/home/vahagndovlatyan/.opencode/bin:$PATH

# ===== cargo =====
. "$HOME/.cargo/env"

# ===== git autocomplete =====
source /usr/share/bash-completion/completions/git


# ===== if not running interactively, don't do anything =====
[[ $- != *i* ]] && return


# history stuff
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000


# ===== make less more friendly for non-text input files, see lesspipe(1) =====
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"


# ===== colored prompt setup with git =====
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        color_prompt=yes
    else
        color_prompt=
    fi
fi

git_branch() {
    if git rev-parse --is-inside-work-tree &>/dev/null; then
        local branch
        branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
        local dirty=""
        [[ -n $(git status --porcelain 2>/dev/null) ]] && dirty="*"
        local upstream=""
        local ahead behind
        ahead=$(git rev-list --left-right --count @{upstream}...HEAD 2>/dev/null | awk '{print $2}')
        behind=$(git rev-list --left-right --count @{upstream}...HEAD 2>/dev/null | awk '{print $1}')
        [[ $ahead -gt 0 ]] && upstream+="↑$ahead"
        [[ $behind -gt 0 ]] && upstream+="↓$behind"
        echo " ($branch$dirty$upstream)"
    fi
}

if [ "$color_prompt" = yes ]; then
	PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\[\033[01;33m\]$(git_branch)\[\033[00m\]\$ '
else
    PS1='\u@\h:\w$(git_branch)\$ '
fi

unset color_prompt force_color_prompt


# ===== neovim terminal =====
nterm() {
  local dir="${1:-.}"
  nvim "$dir" -c "set nospell | terminal"
}


# ===== useful aliases =====
alias ls='ls --color=auto'
alias ll='ls -AlF'
alias la='ls -A'
alias l='ls -CF'
alias lh='ls -d .*'

alias icat='kitty +kitten icat'

alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

alias bat='batcat'

alias gs='git status'


# ===== to fix kitty pointer size, doesnt fix it =====
# alias kitty="XCURSOR_SIZE=16 kitty"

