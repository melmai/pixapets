const favorites = document.querySelectorAll('.favorite');

favorites.forEach(favorite => {
    favorite.addEventListener('click', (e) => {
        e.preventDefault();
        const petID = favorite.dataset.pet;
        const userID = favorite.dataset.user;
        console.log(petID);
        console.log(userID);

        if (userID) {
            fetch(`/favorite/${petID}/${userID}`)
            .then(res => res.json())
            .then(data => {
                const result = data;
                console.log(result);
                if (result) {
                    favorite.classList.toggle('favorite-active');
                }
            })
        } else {
            window.location.href = "/register";
        }
    });
});