// 获取元素
const background = document.getElementsByClassName('background')
const ground = document.getElementsByClassName('ground')
const bird = document.getElementsByClassName("bird")
const text = document.getElementById('text')
const curve = document.getElementById('curve')
// 获取用户滚动页面的
window.addEventListener('scroll', () => {
  const value = window.scrollY
  
  background[0].style.transform = `scaleY(${1 + value * 0.0035})` //背景沿y轴拉伸
  background[0].style.transform = `translateY(${value * -0.5}px)` // 背景往上移动
  
  ground[0].style.transform = `scaleY(${1 - value * 0.0015})`
  ground[0].style.transform = `translateY(${value * 0.15 }px)`
  
  bird[0].style.opacity = 1 - value * 0.0025
  bird[0].style.transform = `translateY(${value * -0.1}px)`

  text.style.transform = `translateY(${value * 0.5}px)`
  text.style.opacity = 1 - value * 0.0025

  curve.style.transform = `scaleY(${2 - value * 0.0015})`
})

function parallax(){
    // 跳出正在施工的提示并置顶显示
    alert("正在施工中，敬请期待！");
  }