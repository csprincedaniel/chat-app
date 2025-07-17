import Image from "next/image";
import Link from "next/link"

export default function Home() {
  return (
    <div>
      <h1>Welcome To OurChat!</h1>

      <div id='wrapper'>
          <div id="container">
              <Link href="/login">
                  <button><h2>Login</h2></button>
              </Link>

              <Link href="/signup">
                  <button><h2>Signup</h2></button>
              </Link>
          </div>
      </div>

      <h1>Created By: Daniel Prince and Jack Tsui.</h1>
    </div>
  );
}
