async function likeFeature(username, friendName) {
  const likeBtn = document.getElementById("like-friend-btn");
  const likeCount = document.getElementById("like-friend-count");

  if (!likeBtn || !likeCount || !friendName) return;

  let isLiked = false;
  let totalLikes = 0;

  function updateLikeUI() {
    likeBtn.textContent = isLiked ? "💔" : "❤️";
    likeCount.textContent = totalLikes;
  }

  //STEP 1: LOAD current likes (no toggle)
  try {
    const res = await fetch("/dash_api/like", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        friend: friendName,
        action: "get"
      })
    });

    const data = await res.json();

    if (res.ok) {
      isLiked = data.liked;
      totalLikes = data.total_likes;
      updateLikeUI();
    }

  } catch (err) {
    console.error("Initial load error:", err);
  }

  // STEP 2: TOGGLE on click
  likeBtn.addEventListener("click", async () => {
    try {
      const res = await fetch("/dash_api/like", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          friend: friendName
        })
      });

      const data = await res.json();

      if (res.ok) {
        isLiked = data.liked;
        totalLikes = data.total_likes;
        updateLikeUI();
      }

    } catch (err) {
      console.error("Like error:", err);
    }
  });
}



async function thumbsUp(username, friendName, activity_id) {
  console.log("entered thumbs up");
  const likeBtn = document.getElementById("like-friend-btn");
  const likeCount = document.getElementById("like-friend-count");

  if (!likeBtn || !likeCount || !friendName) return;

  let isLiked = false;
  let totalLikes = 0;

  //STEP 1: LOAD current likes (no toggle)
  try {
    const res = await fetch("/dash_api/thumbsUp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        friend: friendName,
        action: "get",
        activity_id: activity_id
      })
    });

    const data = await res.json();

    if (res.ok) {
      isLiked = data.liked;
      totalLikes = data.total_likes;
    }

  } catch (err) {
    console.error("Initial load error:", err);
  }

  // STEP 2: TOGGLE on click
  likeBtn.addEventListener("click", async () => {
    try {
      const res = await fetch("/dash_api/thumbsUp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          friend: friendName,
          activity_id: activity_id
        })
      });

      const data = await res.json();

      if (res.ok) {
        isLiked = data.liked;
        totalLikes = data.total_likes;
        updateLikeUI();
      }

    } catch (err) {
      console.error("Like error:", err);
    }
  });
}
