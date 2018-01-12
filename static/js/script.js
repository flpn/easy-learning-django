$(document).ready(() => {
    function updateText(btn, newCount) {
        btn.setAttribute('data-likes', newCount) 
        btn.text = newCount + " Avaliar"
    }

    $('.like-btn').click((evt) => {
        evt.preventDefault()

        var this_ = evt.target
        var likeUrl = this_.getAttribute('data-href')
        var likeCount = parseInt(this_.getAttribute('data-likes'))
        var addLike = likeCount + 1
        var removeLike = likeCount - 1
        
        if(likeUrl) {
            $.ajax({
                url: likeUrl,
                method: 'GET',
                success: (data) => {                            
                    if(data.liked) {
                        updateText(this_, addLike)
                    }
                    else {
                        updateText(this_, removeLike)                                
                    }
                },
                error: (error) => {
                    alert('Você precisa estar logado para votar!')
                    console.log('error')
                }
            })
        }
    })
})