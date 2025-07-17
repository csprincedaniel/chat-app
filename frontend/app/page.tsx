import Image from "next/image";

export default function Home() {
  return (
    <div>
      <h1>Welcome To OurChat!</h1>

      <div id='wrapper'>
          <div id="container">
              <button><h2>Login</h2></button>
              <button><h2>Signup</h2></button>
          </div>
      </div>

      <h1>Created By: Daniel Prince and Jack Tsui.</h1>
    </div>
  );
}
