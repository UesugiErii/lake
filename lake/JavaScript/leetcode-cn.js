// https://leetcode-cn.com/problemset/all/?status=%E6%9C%AA%E5%81%9A
// 用来统计还剩下多少需要会员的题目没做

var sum = 0;
var pre = 1;
var next = 1;

// 回到第一页
while(document.getElementsByClassName('reactable-previous-page').length){
    document.getElementsByClassName('reactable-previous-page')[0].click();
    pre += 1;
}

// 遍历至最后一页
while(document.getElementsByClassName('reactable-next-page').length){
    sum += document.getElementsByClassName('unlock__3Uc0').length;
    document.getElementsByClassName('reactable-next-page')[0].click();
    next += 1;
}

// 返回之前页面
var back = next - pre;
while(back){
    document.getElementsByClassName('reactable-previous-page')[0].click();
    back -= 1;
}

console.log(sum);
