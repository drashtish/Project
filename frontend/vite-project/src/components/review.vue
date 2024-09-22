<template>
  <div>
  <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/UD" class="nav-link">Home</RouterLink>
        <a @click="ulogout" class="nav-link">Logout</a>

      </div>
    </nav>
  <div class="review-container">
    <h3>Leave a Review</h3>
    <p class="average-review">Average Rating: {{ avg }}</p>

    <form @submit.prevent="entry">
      <label for="rating-slider">Rating:</label>
      <input 
        type="range" 
        id="rating-slider" 
        v-model="rev" 
        min="1" 
        max="5" 
        step="1" 
        class="slider" 
        required
      >
      <div class="slider-labels">
        <span v-for="n in 5" :key="n">{{ n }}</span>
      </div>
      <p class="selected-rating">Selected Rating: {{ rev }}</p>

      <button type="submit" class="submit-button">Submit</button>
    </form>
  </div>
  </div>
</template>



<script>
export default {
    name: 'review',
    data() {
        return{
            rev:"",
            id:parseInt(this.$route.params.id,10),
            token:"",
            role:"",
            avg:0,
            sec :""
        };
    },
    methods: {
      ulogout(){
        localStorage.clear()
        alert('You have been logged out successfully')
        this.$router.push('/')
  },
    async entry() {
      try {
        const output = await fetch(`http://localhost:5000/rev/${this.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': `${this.token}`
          },
          body: JSON.stringify({
            rev: this.rev
          })
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        console.log(data);
        this.$router.push(`/usersbooks/${this.sec}`);
        alert(data.msg);

      } catch (error) {
        alert(error.msg);
      }
    },
    async getrev(id) {
      try {
        const output = await fetch(`http://localhost:5000/rev/${this.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': `${this.token}`
          }
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        this.rev = data.data.review;
        this.sec = data.sec,
        this.avg = data.avg

      } catch (error) {
        alert(error.msg);
      }
    }

},
beforeMount(){
    this.token = localStorage.getItem('token')
    this.role = localStorage.getItem('role')
    if (this.token) {
          this.getrev();
      }
    else{
      this.$router.push('/')
      alert(' Token required to enter the site ')
    }
}
    

}
    
</script>



<style scoped>


.navbar {
  width: 100%;
  background-color: #007bff;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: flex-end;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  padding: 0 15px;
  transition: color 0.3s;
  font-size: 20px;
}

.nav-link:hover {
  color: #ffdd57;
}

.review-container {
  max-width: 400px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 100px;
  margin-left: 400px;
}

h3 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.average-review {
  text-align: center;
  font-size: 18px;
  color: #777;
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

.slider {
  width: 100%;
  margin: 20px 0;
  cursor: pointer;
  appearance: none;
  height: 10px;
  border-radius: 5px;
  background: #ddd;
  outline: none;
  transition: background 0.3s;
}

.slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #007bff;
  cursor: pointer;
  transition: background 0.3s;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #007bff;
  cursor: pointer;
  transition: background 0.3s;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #777;
  margin-top: -10px;
}

.selected-rating {
  text-align: center;
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>