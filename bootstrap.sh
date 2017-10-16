sudo apt update
sudo apt -y install build-essential
sudo apt -y install libx11-dev
sudo apt -y install xorg-dev
sudo apt -y install libperl4-corelibs-perl

wget -q -O ns-allinone-2.35.tar.gz https://downloads.sourceforge.net/project/nsnam/allinone/ns-allinone-2.35/ns-allinone-2.35.tar.gz
tar xvzf ns-allinone-2.35.tar.gz
cd ns-allinone-2.35
sudo sed -i '137s/.*/void eraseAll() { this->erase(baseMap::begin(), baseMap::end()); }/' ns-2.35/linkstate/ls.h
sudo ./install

echo PATH="$PATH:/home/ubuntu/ns-allinone-2.35/bin:/home/ubuntu/ns-allinone-2.35/tcl8.5.10/unix:/home/ubuntu/ns-allinone-2.35/tk8.5.10/unix" >> ~/.profile
. ~/.profile
