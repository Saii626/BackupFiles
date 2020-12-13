#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# run these irrespective of interactive or not
export EDITOR="nvim"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

alias ls='ls --color=auto'
export PS1="\h@\u:\w\nλ "

# autocomplete for sudo
complete -cf sudo


alias proj='cd /media/Data/Projects'
alias soft='cd /media/Data/Softwares'

shopt -s autocd
shopt -s cdspell
shopt -s checkjobs

# bash history config
export HISTCONTROL=ignoreboth:erasedups
export HISTSIZE=5000
shopt -s histappend

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="/home/saii/.sdkman"
[[ -s "/home/saii/.sdkman/bin/sdkman-init.sh" ]] && source "/home/saii/.sdkman/bin/sdkman-init.sh"
