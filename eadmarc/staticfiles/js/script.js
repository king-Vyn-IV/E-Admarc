<script>
document.addEventListener('DOMContentLoaded', () => {
  const newsletterForm = document.querySelector('footer form');
  const emailInput = newsletterForm.querySelector('input[type="email"]');

  newsletterForm.addEventListener('submit', (e) => {
    e.preventDefault(); // prevent page reload

    const email = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email) {
      alert('Please enter your email address.');
      return;
    }

    if (!emailRegex.test(email)) {
      alert('Please enter a valid email address.');
      return;
    }

    // Simulate a successful submission (replace with AJAX call if needed)
    alert(`Thank you for subscribing with ${email}!`);
    emailInput.value = ''; // clear the input
  });
});
</script>
