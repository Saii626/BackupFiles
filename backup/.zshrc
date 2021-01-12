# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -v
export KEYTIMEOUT=1
# End of lines configured by zsh-newuser-install

autoload -Uz compinit
zstyle ':completion:*' menu select
compinit
_comp_options+=(globdots)

export EDITOR="nvim"

alias ls='ls --color=auto'

alias proj='cd /media/Data/Projects'
alias soft='cd /media/Data/Softwares'

bindkey "^[[A" history-beginning-search-backward
bindkey "^[[B" history-beginning-search-forward

export NVM_DIR="$HOME/.config/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# Change cursor shape for different vi modes.
function zle-keymap-select {
  if [[ ${KEYMAP} == vicmd ]] ||
     [[ $1 = 'block' ]]; then
    echo -ne '\e[1 q'
  elif [[ ${KEYMAP} == main ]] ||
       [[ ${KEYMAP} == viins ]] ||
       [[ ${KEYMAP} = '' ]] ||
       [[ $1 = 'beam' ]]; then
    echo -ne '\e[5 q'
  fi
}
zle -N zle-keymap-select
zle-line-init() {
    zle -K viins # initiate `vi insert` as keymap (can be removed if `bindkey -V` has been set elsewhere)
    echo -ne "\e[5 q"
}
zle -N zle-line-init
echo -ne '\e[5 q' # Use beam shape cursor on startup.
preexec() { echo -ne '\e[5 q' ;} # Use beam shape cursor for each new prompt.

n () {
    # Block nesting of nnn in subshells
    if [ -n $NNNLVL ] && [ "${NNNLVL:-0}" -ge 1 ]; then
        echo "nnn is already running"
        return
    fi

    # The default behaviour is to cd on quit (nnn checks if NNN_TMPFILE is set)
    # To cd on quit only on ^G, remove the "export" as in:
    #     NNN_TMPFILE="${XDG_CONFIG_HOME:-$HOME/.config}/nnn/.lastd"
    # NOTE: NNN_TMPFILE is fixed, should not be modified
    export NNN_TMPFILE="${XDG_CONFIG_HOME:-$HOME/.config}/nnn/.lastd"

    # Unmask ^Q (, ^V etc.) (if required, see `stty -a`) to Quit nnn
    # stty start undef
    # stty stop undef
    # stty lwrap undef
    # stty lnext undef

    nnn "$@"

    if [ -f "$NNN_TMPFILE" ]; then
            . "$NNN_TMPFILE"
            rm -f "$NNN_TMPFILE" > /dev/null
    fi

    export NNN_SSHFS='sshfs -o reconnect,cache_timeout=3600'

    export NNN_FIFO=/tmp/nnn.fifo
    
    export USE_SCOPE=1
    export USE_VIDEOTHUMB=1

    export NNN_PLUG='p:preview-tui'
}

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="/home/saii/.sdkman"
[[ -s "/home/saii/.sdkman/bin/sdkman-init.sh" ]] && source "/home/saii/.sdkman/bin/sdkman-init.sh"

# Denote whether we are inside screen/tmux or not
NEWLINE=$'\n'
PS1="%M:%n%~ ${NEWLINE}λ "
if [ -n "$STY" ]; then export PS1="(screen) $PS1"; fi
if [ -n "$TMUX" ]; then export PS1="(tmux) $PS1"; fi

source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.plugin.zsh

