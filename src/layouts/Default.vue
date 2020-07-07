<template>
  <div class="layout">
    <noscript v-html="`<div id='noscript'>This site requires javascript.</div>`"/>
    <video autoplay muted loop id="myVideo">
      <source src="/currency_video.mp4" type="video/mp4" preload="auto"/>
    </video>
    <!-- <header class="header">
      <strong>
        <g-link to="/">{{ $static.metadata.siteName }}</g-link>
      </strong>
      <nav class="nav">
        <g-link class="nav__link" to="/">Home</g-link>
      </nav>
    </header>-->
    <slot />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}
* + * {
  margin-top: 0;
  margin-bottom: 0.5rem;
}
body {
  font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.5;
}
#myVideo {
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  z-index: -1;
  margin: 0;
}
p {
  font-size: 1.5rem;
  margin-bottom: 1.25rem;
}
#noscript {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 0.5rem;
  color: #fff;
  text-align: center;
  z-index: 999999;
  background: red;
}
</style>
