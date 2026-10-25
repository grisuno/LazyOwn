#!/bin/bash
echo 'LazyOwn cleaning bash history [;,;]'
rm -fv ~/.bash_history
sudo rm -fv /root/.bash_history
echo 'LazyOwn cleaning Zsh history [;,;]'
rm -fv ~/.zsh_history
sudo rm -fv /root/.zsh_history
echo 'LazyOwn cleaning tcsh history [;,;]'
rm -fv ~/.history
sudo rm -fv /root/.history
echo 'LazyOwn cleaning fish history [;,;]'
rm -fv ~/.local/share/fish/fish_history
sudo rm -fv /root/.local/share/fish/fish_history
rm -fv ~/.config/fish/fish_history
sudo rm -fv /root/.config/fish/fish_history
echo 'LazyOwn cleaning KornShell (ksh) history [;,;]'
rm -fv ~/.sh_history
sudo rm -fv /root/.sh_history
echo 'LazyOwn cleaning ash history [;,;]'
rm -fv ~/.ash_history
sudo rm -fv /root/.ash_history
echo 'LazyOwn cleaning crosh history [;,;]'
rm -fv ~/.crosh_history
sudo rm -fv /root/.crosh_history
