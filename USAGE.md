# Spotify Stats Widget - Usage Guide

A live Spotify widget that displays your currently playing song and top tracks on your GitHub README.

## 🚀 Quick Start

### 1. Currently Playing / Recent Track

Shows what you're listening to right now (or your last played track):

```markdown
[![Spotify](https://spotify-stats-q7nq.vercel.app/)](https://open.spotify.com/user/YOUR_SPOTIFY_USERNAME)
```

**Preview:**  
Displays album art, song name, artist, and animated equalizer bars.

---

### 2. Top 5 Tracks (Last 4 Weeks)

Shows your most-played songs from the past month:

```markdown
![Top Tracks](https://spotify-stats-q7nq.vercel.app/top-tracks)
```

**Preview:**  
Lists your top 5 tracks with song names and artists.

---

## 🎨 Customization

Both endpoints support custom colors via URL parameters:

### Background & Border Colors

```markdown
<!-- Dark theme -->
![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=0d1117&border_color=ffffff)

<!-- Green theme -->
![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=1DB954&border_color=000000)

<!-- Top tracks with custom colors -->
![Top Tracks](https://spotify-stats-q7nq.vercel.app/top-tracks?background_color=282828&border_color=1DB954)
```

**Parameters:**
- `background_color` - Hex color without `#` (default: `181414`)
- `border_color` - Hex color without `#` (default: `181414`)

---

## 📋 Complete README Example

```markdown
## 🎵 Spotify Activity

### Currently Listening To
[![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=0d1117&border_color=1DB954)](https://open.spotify.com/user/YOUR_USERNAME)

### 🔥 Top Tracks (Last 4 Weeks)
![Top Tracks](https://spotify-stats-q7nq.vercel.app/top-tracks?background_color=0d1117&border_color=1DB954)
```

---

## 🔄 Cache & Updates

- **Currently Playing**: Updates every second (Cache: 1 second)
- **Top Tracks**: Updates every hour (Cache: 1 hour)

---

## 🎭 Theme Examples

### GitHub Dark Theme
```markdown
![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=0d1117&border_color=30363d)
```

### Spotify Green Theme
```markdown
![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=191414&border_color=1DB954)
```

### Light Theme
```markdown
![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=ffffff&border_color=000000)
```

### Transparent-ish
```markdown
![Spotify](https://spotify-stats-q7nq.vercel.app/?background_color=00000000&border_color=1DB954)
```

---

## 🛠️ Available Themes

The widget supports two template themes in `api/templates.json`:

- **dark** → `spotify-dark.html.j2` (default)
- **light** → `spotify.html.j2`

To switch themes, update `current-theme` in `api/templates.json` and redeploy.

---

## 📌 Tips for README

1. **Add a clickable link** - Wrap the widget in a link to your Spotify profile:
   ```markdown
   [![Spotify](https://spotify-stats-q7nq.vercel.app/)](https://open.spotify.com/user/YOUR_USERNAME)
   ```

2. **Stack widgets vertically** - Use multiple line breaks for better spacing:
   ```markdown
   ### Now Playing
   ![Spotify](https://spotify-stats-q7nq.vercel.app/)
   
   ### Top Tracks
   ![Top Tracks](https://spotify-stats-q7nq.vercel.app/top-tracks)
   ```

3. **Align center** - Use HTML for centered widgets:
   ```html
   <div align="center">
     <img src="https://spotify-stats-q7nq.vercel.app/" alt="Spotify">
   </div>
   ```

4. **Match your README theme** - Use color parameters that match your existing color scheme.

---

## 🐛 Troubleshooting

### Widget not updating?
- GitHub caches images. Add `?v=1` to force refresh: `...vercel.app/?v=1`
- Hard refresh your browser (Ctrl+Shift+R / Cmd+Shift+R)

### Shows "Recently played" instead of current track?
- Make sure you're actively playing music on Spotify
- Check that your Spotify session is not in private mode

### 500 Error?
- Verify environment variables are set in Vercel dashboard
- Check Vercel deployment logs for errors

---

## 🔗 Endpoints

| Endpoint | Description | Cache |
|----------|-------------|-------|
| `/` | Currently playing or recent track | 1 second |
| `/top-tracks` | Top 5 tracks from last 4 weeks | 1 hour |

---

## 📦 What's Needed

To set up your own instance:

1. **Spotify App** (Client ID & Secret)
2. **Refresh Token** (OAuth flow)
3. **Vercel Account** (for deployment)

See `SetUp.md` for detailed setup instructions.

---

## 🎯 Color Palette Ideas

| Theme | Background | Border |
|-------|------------|--------|
| GitHub Dark | `0d1117` | `30363d` |
| Spotify Classic | `191414` | `1DB954` |
| Dracula | `282a36` | `bd93f9` |
| Nord | `2e3440` | `88c0d0` |
| Monokai | `272822` | `a6e22e` |

---

Made with ❤️ using Flask, Spotify API, and Vercel
