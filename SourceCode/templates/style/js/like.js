// document.addEventListener("DOMContentLoaded", () => {
//   const username = localStorage.getItem("currentUser");

//   if (username) {
//     const nameEl = document.getElementById("user-name");
//     if (nameEl) nameEl.textContent = username;
//   }

//   likeFeature(username);
// });


// function likeFeature(username) {
//   const likeBtn = document.getElementById("like-friend-btn");
//   const likeCount = document.getElementById("like-friend-count");

//   if (!likeBtn || !likeCount) return; // safety

//   let isLiked = false;
//   let totalLikes = parseInt(likeCount.textContent) || 0;

//   // If you have the friend info in a data attribute
//   // e.g., <div id="friend-profile" data-username="friendUsername">
//   const friendProfileEl = document.getElementById("friend-profile");
//   let currentFriend = null;
//   if (friendProfileEl) {
//     currentFriend = friendProfileEl.dataset.username;
//   }

//   if (!currentFriend) {
//     console.warn("No friend info found! Add data-username attribute.");
//     return;
//   }

//   // Initialize UI (optional, in case initial likes are loaded)
//   updateLikeUI();

//   function updateLikeUI() {
//     likeBtn.textContent = isLiked ? "💔" : "❤️";
//     likeCount.textContent = totalLikes;
//   }

//   likeBtn.addEventListener("click", async () => {
//     if (!currentFriend) return;

//     console.log("Like clicked for:", currentFriend);

//     try {
//       const res = await fetch("/dash_api/like", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           username,
//           friend: currentFriend
//         })
//       });

//       const data = await res.json();
//       console.log("Like API response:", data);

//       if (res.ok) {
//         isLiked = data.liked;
//         totalLikes = data.total_likes;
//         updateLikeUI();
//       } else {
//         console.error(data.message);
//       }

//     } catch (err) {
//       console.error("Like error:", err);
//     }
//   });
// }
