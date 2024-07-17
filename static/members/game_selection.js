// 切換容器效果
document.addEventListener('DOMContentLoaded', function () { // 整個DOM文檔加載完畢並解析完成後執行內部函數
    const toggleButton = document.getElementById('toggleButton');   // 獲取切換按鈕
    const hbContainer = document.querySelector('.hb_container');    // 獲取 hb_container 容器
    const hsContainer = document.querySelector('.hs_container');    // 獲取 hsContainer 容器

    // 初次加載時只顯示 hb_container
    hbContainer.style.display = 'block';    // 設置 hb_container 的 display 為 'block' 使其顯示
    hbContainer.style.opacity = 1;  // 設置 hb_container 的透明度為 1

    // 設置切換按鈕的點擊事件處理函數
    toggleButton.addEventListener('click', function () {
        if (hbContainer.classList.contains('active')) { // 檢查 hb_container 是否包含 active
            hbContainer.classList.remove('active'); // 移除 hb_container 的 active
            hbContainer.style.opacity = 0;  // 設置 hb_container 的透明度為 0
            setTimeout(function () {    // 設置一個 500 毫秒後執行的定時器
                hbContainer.style.display = 'none'; // 設置 hb_container 的 display 為 'none' 使其隱藏
                hsContainer.style.display = 'block';    // 設置 hsContainer 的 display 為 'block' 使其顯示
                setTimeout(function () {    // 再設置一個 10 毫秒後執行的定時器
                    hsContainer.style.opacity = 1;  // 設置 hsContainer 的透明度為 1
                    hsContainer.classList.add('active');    // 添加 hsContainer 的 active
                }, 10);
            }, 500);
        } else {
            // 與上面相反的過程，將 hsContainer 切換到 hb_container
            hsContainer.classList.remove('active');
            hsContainer.style.opacity = 0;
            setTimeout(function () {
                hsContainer.style.display = 'none';
                hbContainer.style.display = 'block';
                setTimeout(function () {
                    hbContainer.style.opacity = 1;
                    hbContainer.classList.add('active');
                }, 10);
            }, 500);
        }
    });
});