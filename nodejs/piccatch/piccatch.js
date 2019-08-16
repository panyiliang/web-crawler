const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const request = require('request');
const dirname = 'uploadImages'
const hostdir = "./img/"
//初始url 
var url = "https://lovecomicz.com/ero_books/33630"; 
function startSpider(x) {
    console.log('向目标站点发送请求');
    //采用http模块向服务器发起一次get请求      
    https.get(x, function (res) {     
        var html = '';        //用来存储请求网页的整个html内容
        var titles = [];        
        res.setEncoding('utf-8'); //防止中文乱码
        //监听data事件，每次取一块数据
        res.on('data', function (chunk) {   
            html += chunk;
            //console.log(chunk)
        });
        //监听end事件，如果整个网页内容的html都获取完毕，就执行回调函数
        res.on('end', function () {

        var $ = cheerio.load(html); //采用cheerio模块解析html
        var arr = new Array();
        $('.post_content img').each(function(){
          var src=$(this).attr("src");
          var img_filename = $(this).attr("srcset");
          console.log('img_filename:'+img_filename);
          console.log('src:'+src);
          const url = src;
          const first = url.indexOf(dirname)
          const last = url.lastIndexOf('/')
          if (first > 0 && last > 0) {
            const name = url.substr(last + 1)
            const dir = url.substr(first, last - first)
            const dstpath = hostdir + dir + '/' + name
            if (name.length && dir.length && !fs.existsSync(dstpath)) {
              if (mkdirSync(hostdir + dir)) {
                console.log(dstpath)
                request(url).pipe(fs.createWriteStream(dstpath))
              }
            }
          }
          })
        });
    }).on('error', function (err) {
        console.log(err);
    });

}

function mkdirSync(dirname) {
    if (fs.existsSync(dirname)) {
        return true;
    } else {
        if (mkdirSync(path.dirname(dirname))) {   
            fs.mkdirSync(dirname);
            return true;
        }
    }
    return false
}

startSpider(url);      //主程序开始运