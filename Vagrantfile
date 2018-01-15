# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "grocer" do |grocer|
    grocer.vm.box = "wepiao/ubuntu14.04_docker"
    grocer.vm.box_url = "http://pypi.wepiao.com/static/boxes/ubuntu/metadata.json"
    grocer.vm.hostname = "vagrant-grocer.vm"
    grocer.vm.network "private_network", ip: "192.168.50.80"
    config.vm.synced_folder ".", "/data/apps/grocer"
    grocer.vm.provider "virtualbox" do |vb|
      vb.name = "vagrant-grocer"
      vb.cpus = 2
      vb.memory = 2*1024
    end
    grocer.ssh.insert_key = false
  end
  config.vm.provision "shell", privileged:false, inline: <<-SHELL
    cd /data/apps/grocer/
    test -e env || virtualenv env
    test -e logs || mkdir logs
    ln -s /data/apps/grocer/pip.conf /data/apps/grocer/env/pip.conf
    source /data/apps/grocer/env/bin/activate
    pip install -r requirements.txt
  SHELL

  config.vm.provision "shell", privileged:false, run: "always", inline: <<-SHELL
    date
    echo "The envrioment of project grocer is ready.My Lord."
  SHELL

  config.push.define "local-exec" do |push|
    push.inline = <<-SCRIPT
      scp ./ubuntu14.04_docker.box tecs:/tmp/ubuntu14.04_docker.box
    SCRIPT
  end
end
