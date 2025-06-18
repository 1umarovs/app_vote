// static/js/discussion_ajax.js

// ------- LIKE (Vote) Toggle -------
document.addEventListener("click", function (e) {
    if (e.target.closest(".vote-form")) {
        e.preventDefault();
        const form = e.target.closest("form");
        const url = form.action;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
        .then((res) => res.text())
        .then(() => {
            // Reload partial list
            reloadDiscussionList();
        });
    }
});

// ------- Submit Discussion -------
document.querySelector(".form form")?.addEventListener("submit", function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    fetch("", {
        method: "POST",
        body: formData,
    })
        .then((res) => res.text())
        .then(() => {
            reloadDiscussionList();
            form.reset();
        });
});

// ------- Filtering -------
document.querySelectorAll(".dropdown-menu a").forEach((link) => {
    link.addEventListener("click", function (e) {
        e.preventDefault();
        const url = new URL(window.location);
        const params = new URLSearchParams(url.search);
        const href = new URL(e.target.href);

        for (const [key, value] of href.searchParams) {
            params.set(key, value);
        }

        history.pushState({}, "", `?${params.toString()}`);
        reloadDiscussionList();
    });
});

// ------- Pagination -------
document.addEventListener("click", function (e) {
    if (e.target.closest(".pagination a")) {
        e.preventDefault();
        const pageUrl = new URL(e.target.href);
        const params = new URLSearchParams(pageUrl.search);

        history.pushState({}, "", `?${params.toString()}`);
        reloadDiscussionList();
    }
});

// ------- Load Discussions with AJAX -------
function reloadDiscussionList() {
    const url = window.location.href;

    fetch(url, {
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
        .then((res) => res.text())
        .then((html) => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newList = doc.querySelector(".lists");
            const newPagination = doc.querySelector(".pagination");

            document.querySelector(".lists").innerHTML = newList.innerHTML;
            document.querySelector(".pagination").innerHTML = newPagination.innerHTML;
        });
}
