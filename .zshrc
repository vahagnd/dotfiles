# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export PATH="/opt/homebrew/bin:$PATH"

# History settings
HISTSIZE=1000
SAVEHIST=2000
setopt append_history
setopt hist_ignore_dups
setopt hist_ignore_space

# lesspipe (check if works or comment out)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# Colored prompt
PS1='%F{green}%n@%m%f:%F{blue}%~%f$ '

## source env
# . "$HOME/.local/bin/env"

# Aliases
alias ls='ls -G'
alias ll='ls -AlF'
alias la='ls -A'
alias l='ls -CF'
alias lh='ls -d .*'

alias icat='kitty +kitten icat'

alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# alias kitty="XCURSOR_SIZE=16 kitty"

