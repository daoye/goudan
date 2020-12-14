# goudan(狗蛋)

Goudan(狗蛋)is a tunnel proxy, it's support all tcp proxy(theoretically), such as http,https,socks.
By default, goudan crawl free proxies from some websites. So, you can use it out of box.

## Why do this

When I develop a spider to crawl some web sites, most time they have some defense measures.

So, I must change my IP to crawl it at a moment.

The best way is set a proxy address for a web requests libray, such as "Requests","urlib", "aiohttp" and so on.

But, I need write those code in every project. And I want't to do this.

This why I start this project.

## How to use

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
