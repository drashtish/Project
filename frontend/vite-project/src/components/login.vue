<template>
    <div class="container">
      <h3> Login Form </h3>
        <form @submit.prevent>
            <div class="form">
                <label class="form-label" for="email">Email:</label>
                <input type="email" v-model="email" class="form-control" id="email" required>

                <label class="form-label" for="password">Password:</label>
                <input type="password" v-model="password" class="form-control" id="password" required>

                <button @click="entry" class="btn-primary">Submit</button>
            </div>

            <div id="signUpLink">
                <p>Don't have an account? <a href="/register" class="btn-link">Sign Up</a></p>
                <p>Are you an Admin? <a href="/adminlogin" class="btn-link">Admin Login</a></p>
            </div>
        </form>
    </div>
</template>


<script>
export default {
  name: 'login',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async entry() {
      try {
        const output = await fetch('http://localhost:5000/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.message || 'An error occurred');
        }

        const data = await output.json();
        console.log(data);
        localStorage.setItem('token', data.token)
        localStorage.setItem('role', data.role)
        this.$router.push('/UD')

      } catch (error) {
          alert(error.message)
      }
    }
  }
}
</script>

<style scoped>
body {
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f4f4f4;
    margin: 0; 
}

.container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
    width: 500px;
    padding: 30px;
    text-align: center;

}

.form {
    display: block;
    font-size: 18px;
    text-align: left;
}

.form-label {
    display: block;
    font-weight: bold;
    margin-bottom: 10px;
}

.form-control {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 20px;
    transition: border-color 0.3s;
    background-color: #f5f5f5; 
}

.form-control:hover {
    border-color: #007bff;
}

.btn-primary {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    text-align: center;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.btn-link {
    text-decoration: none;
    cursor: pointer;
    font-size: 16px;
    color: #007bff;
}

.btn-link:hover {
    text-decoration: underline;
}

#signUpLink {
    text-align: center;
    margin-top: 20px;
}

.name {
    text-align: center;
}

.al {
    color: white;
    padding: 5px;
}

</style>
