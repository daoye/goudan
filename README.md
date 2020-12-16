# goudan(狗蛋)

Goudan(狗蛋)is a tunnel proxy, it's support all tcp proxy(theoretically), such as http,https,socks.
By default, goudan crawl free proxies from some websites. So, you can use it out of box.

## How to use

### Install masscan
The plugin 'scanner' use masscan to scan proxy from internal , if you use this plugin, you need install masscan.

On ubuntu, install it by this command:

```bash
sudo apt -y install masscan

````


### Use by docker(Recommend)

```bash
docker run -p 1991:1991 -p 1992:1992 -p 1993:1993 -p 1994:1994 -d --restart unless-stopped --ulimit nofile=2048:2048 --ulimit nproc=1024 --name goudan daoye/goudan
```

or

```bash
docker run -p 1991:1991 -p 1994:1994 -d --restart unless-stopped --ulimit nofile=2048:2048 --ulimit nproc=1024 --name goudan daoye/goudan --log_level 10 -r 10 -l http:0.0.0.0:1991,socks5:0.0.0.0:1994
```

If you want see some help documents:

```bash
docker run --rm daoye/goudan -h
```

### From source(need python3.7)

```bash
git clone https://github.com/daoye/goudan.git
git checkout develop
cd goudan
python3 main.py
```

__The best way is use virtualenv.__

## Write my plugins

Visit: [Goudan_plugins](https://github.com/daoye/goudan_plugins)


## The end

Enjoy!

## License

MIT License
