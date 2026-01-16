# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export PATH="/opt/homebrew/bin:$PATH"
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

export PYTHONPATH="$HOME/Projects/spotify-helper"

# History settings
HISTSIZE=1000
SAVEHIST=2000
setopt append_history
setopt hist_ignore_dups
setopt hist_ignore_space

# lesspipe (check if works or comment out)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

## source env
# . "$HOME/.local/bin/env"

eval "$(direnv hook zsh)"

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

alias ubuntu='docker start ubuntu1 && docker exec -it --user vahagn ubuntu1 bash -c "cd && exec bash"'

alias gs='git status'

# Prompt
setopt prompt_subst

git_branch() {
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo " (%F{yellow}$branch%f)"
    fi
}

PS1='%F{green}%n@%m%f:%F{blue}%~%f$(git_branch)$ '

# Autocompletion
fpath+=~/.zfunc; autoload -Uz compinit; compinit

zstyle ':completion:*' menu select
