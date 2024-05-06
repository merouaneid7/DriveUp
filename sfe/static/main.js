// main.js

fetch('/create_checkout_session/')
  .then(function(response) {
    return response.json();
  })
  .then(function(session) {
    return stripe.redirectToCheckout({ sessionId: session.sessionId });
  })
  .then(function(result) {
    if (result.error) {
      // Handle any errors that occur during redirection to Checkout
      console.error(result.error.message);
    }
  })
  .catch(function(error) {
    console.error('Error:', error);
  });
