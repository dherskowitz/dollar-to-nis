<template>
  <Layout>
    <section class="home">
      <div class="home__inner">
        <h1 class="home__title">Dollar to NIS</h1>
        <p>{{base}} to {{ base == "USD" ? "ILS" : "USD" }}</p>
        <p v-if="isLoading" class="gradient loadingbar1"></p>
        <div v-else>
          <p>{{rate}}</p>
          <div class="exchange">
            <input class="exchange__amount" v-on:keyup="convert" v-model="exchangeAmount"> =
            <span class="exchange__amount">{{exchangeResultFixed}}</span>
          </div>
        </div>
        <div class="changeDirection">
          <input
            @change="changeDirection($event)"
            id="toggle-on"
            class="toggle toggle-left"
            name="toggle"
            value="false"
            type="radio"
            checked
          />
          <label for="toggle-on" class="btn">USD to ILS</label>
          <input
            @change="changeDirection($event)"
            id="toggle-off"
            class="toggle toggle-right"
            name="toggle"
            value="true"
            type="radio"
          />
          <label for="toggle-off" class="btn">ILS to USD</label>
        </div>
        <p v-if="!isLoading" class="last_updated">{{last_updated}}</p>
      </div>
    </section>
  </Layout>
</template>

<script>
export default {
  metaInfo: {
    title: "Dollar to NIS"
  },
  data() {
    return {
      usd: "",
      ils: "",
      base: "USD",
      last_updated: "",
      rate: "",
      direction: "usd-ils",
      isLoading: true,
      exchangeAmount: "1",
      exchangeResult: ""
    };
  },
  computed: {
    exchangeResultFixed: function () {
      return this.exchangeResult.toFixed(2)
    }
  },
  methods: {
    convert() {
      if (this.direction == "usd-ils") {
        this.exchangeResult = parseFloat(this.exchangeAmount) * this.usd;
      } else {
        this.exchangeResult = parseFloat(this.exchangeAmount) * this.ils;
      }
    },
    setData(data) {
      const regex = /am|pm/gi;
      let date = new Date();
      this.last_updated = `Last updated on ${date.toDateString()} at ${date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;
      this.usd = data.USD_ILS;
      this.ils = data.ILS_USD;
      this.rate = `\u0024${this.usd.toFixed(2)} = \u20AA${this.ils.toFixed(2)}`;
      this.isLoading = !this.isLoading;
    },
    setCache(data) {
      localStorage.setItem("last_updated", JSON.stringify(new Date()))
      localStorage.setItem("rates", JSON.stringify(data));
    },
    async getRate() {
      const rate = await fetch("/api/currency");
      const res = await rate.json();
      this.setData(res);
      this.setCache(res);
      this.convert();
    },
    changeDirection(event) {
      if (this.direction == "usd-ils") {
        this.direction = "ils-usd";
        this.base = "ILS";
        this.rate = `\u20AA${this.ils.toFixed(2)} = \u0024${this.usd.toFixed(2)}`;
      } else {
        this.direction = "usd-ils";
        this.base = "USD";
        this.rate = `\u0024${this.usd.toFixed(2)} = \u20AA${this.ils.toFixed(2)}`;
      }
      this.convert();
    },
    hoursSinceUpdated() {
      let last_updated = localStorage.getItem("last_updated").replace(/am|pm/gi, '').trim();
      let last_updated_utc = new Date(`${last_updated} UTC`);
      let now = new Date();
      let diffTime = Math.abs(last_updated_utc - now);
      let diffHours = (diffTime / (1000 * 60 * 60)).toFixed(2);
      return parseFloat(diffHours);
    },
  },
  mounted() {
    if (!localStorage.getItem("last_updated") || this.hoursSinceUpdated() > 4) {
      this.getRate();
    } else {
      this.setData(JSON.parse(localStorage.getItem("rates")));
      this.convert();
    }
  }
};
</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: rgba(255, 255, 255, 0.5);
  margin: 0;
  padding: 0 1rem;
}
.home__title {
  text-transform: uppercase;
  font-size: 2rem;
  margin-top: 0;
}
.home__inner {
  background: rgba(36, 37, 42, 1);
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0px 1px 5px 0px #333;
  max-width: 100%;
  width: 500px;
  text-align: center;
  margin: 0 1rem;
  color: #fff;
}
.last_updated {
  font-size: 0.8rem;
  margin: 0;
}
.exchange {
  font-size: 1.5rem;
  margin-bottom: 1.25rem;
}
.exchange__amount {
  width: 6rem;
  font-size: 1.5rem;
  padding: 5px 0 5px 0.5rem;
  border-radius: 0.25rem;
  border: none;
  margin-right: 0.5rem;
}
@media (max-width: 580px) {
  .home__inner {
    padding: 2rem;
    width: 100%;
  }
}

.loadingbar1 {
  height: 24px;
  border-radius: 1rem;
}

.loadingbar2 {
  height: 19px;
  border-radius: 1rem;
}


.gradient {
  animation-duration: 1.8s;
  animation-fill-mode: forwards;
  animation-iteration-count: infinite;
  animation-name: placeHolderShimmer;
  animation-timing-function: linear;
  background: #f6f7f8;
  background: linear-gradient(to right, #fafafa 8%, #b6b3b3 38%, #fafafa 54%);
  background-size: 1000px 640px;
  /* position: relative; */
}

@keyframes placeHolderShimmer {
  0% {
    background-position: -468px 0;
  }
  100% {
    background-position: 468px 0;
  }
}

.btn {
  border: 3px solid #1a1a1a;
  display: inline-block;
  padding: 10px;
  position: relative;
  text-align: center;
  -webkit-transition: background 600ms ease, color 600ms ease;
  transition: background 600ms ease, color 600ms ease;
}

input[type="radio"].toggle {
  display: none;
}
input[type="radio"].toggle + label {
  cursor: pointer;
  min-width: 60px;
}
input[type="radio"].toggle + label:hover {
  background: none;
  color: #e8e8e8;
}
input[type="radio"].toggle + label:after {
  background: #e8e8e8;
  content: "";
  height: 100%;
  position: absolute;
  top: 0;
  -webkit-transition: left 200ms cubic-bezier(0.77, 0, 0.175, 1);
  transition: left 200ms cubic-bezier(0.77, 0, 0.175, 1);
  width: 100%;
  z-index: -1;
}
input[type="radio"].toggle.toggle-left + label {
  border-right: 0;
}
input[type="radio"].toggle.toggle-left + label:after {
  left: 100%;
}
input[type="radio"].toggle.toggle-right + label {
  margin-left: -5px;
}
input[type="radio"].toggle.toggle-right + label:after {
  left: -100%;
}
input[type="radio"].toggle:checked + label {
  cursor: default;
  color: #000;
  -webkit-transition: color 200ms;
  transition: color 200ms;
  z-index: 1;
}
input[type="radio"].toggle:checked + label:after {
  left: 0;
}
</style>
