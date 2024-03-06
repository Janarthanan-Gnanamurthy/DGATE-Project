<template>
  <main>
    <div class="relative flex flex-col items-center pt-32 h-screen overflow-hidden">
      <div class="w-full p-6 bg-white border-t-4 border-primary rounded-md shadow-md border-top lg:max-w-lg">
        <h1 class="text-3xl font-semibold text-center text-gray-700">Student Login</h1>
        <form class="space-y-4">
          <div>
            <label class="label">
                <span class="text-base label-text">Email</span>
            </label>
            <input type="text" placeholder="Email Address" class="w-full input input-bordered" />
          </div>
          <div>
            <label class="label">
              <span class="text-base label-text">Password</span>
            </label>
            <input type="password" placeholder="Enter Password"
              class="w-full input input-bordered" />
          </div>
          <a href="#" class="text-xs text-gray-600 hover:underline hover:text-blue-600">Forget Password?</a>
          <div>
            <button @click="this.$router.push('/')" class="btn btn-primary w-full text-2xl">Login</button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>