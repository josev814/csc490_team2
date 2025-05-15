import { render, screen, fireEvent, within } from '@testing-library/react';
import App from '../App';

function removeLoginErrors(){
  // reset invalid creds element
  const invalidCredentialsElement = screen.queryByText(/Invalid Credentials/i);
  if (invalidCredentialsElement) {
    document.getElementById('login_errors').remove()
  }
}
describe("LoginRegister component", () => {
  test("go to login form", async () => {
    render(<App />)
    const loginLink = screen.getByText(/Login/i);
    fireEvent.click(loginLink);
    
    expect(screen.getByText("Account Login")).toBeInTheDocument();
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  test("switches to registration form when 'Register' link is clicked", async () => {
    render(<App />)
    
    const form = screen.getByRole('form')
    const registerLink = within(form).getByRole('link', {name: /Register/i})
    
    fireEvent.click(registerLink);

    expect(screen.getByText("Account Registration")).toBeInTheDocument();
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  test("switches back to login form when 'Log In' link is clicked", async () => {
    render(<App />)

    const form = screen.getByRole('form')
    const loginLink = within(form).getByRole('link', {name: /Log In/i})
    
    fireEvent.click(loginLink);

    expect(screen.getByText("Account Login")).toBeInTheDocument();
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  test("test invalid email login form submission failure", async () => {
    render(<App />)

    const form = screen.getByRole('form')
  
    // Fill in the form fields with invalid data
    fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "invalid-email" } });
    fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "" } });

    // Submit the form
    fireEvent.click(within(form).getByText("Login"));

    // Assert that the error message is displayed
    expect(await screen.findByText(/Invalid Credentials/i)).toBeInTheDocument();

  });

  test("test missing password login form submission failure", async () => {
    render(<App />)
    // reset invalid creds element
    removeLoginErrors()
    const form = screen.getByRole('form')
    
  
    fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123" } });
    fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "" } });

    // Submit the form
    fireEvent.click(within(form).getByText("Login"));
    
    // Assert that the error message is displayed
    expect(await screen.findByText(/Invalid Credentials/i)).toBeInTheDocument();
  });

  test("test short password login form submission failure", async () => {
    render(<App />)
    removeLoginErrors()
    const form = screen.getByRole('form')
  
    fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123" } });
    fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "asdf" } });

    // Submit the form
    fireEvent.click(within(form).getByText("Login"));  
    
    // Assert that the error message is displayed
    expect(await screen.findByText(/Invalid Credentials/i)).toBeInTheDocument();
  });

//   test("submits login form with correct data", () => {
//     const { getByLabelText, getByText, getByTestId } = render(<LoginRegister />);
  
//     // Fill in the form fields
//     fireEvent.change(getByLabelText("Email address"), { target: { value: "test@example.com" } });
//     fireEvent.change(getByLabelText("Password"), { target: { value: "password123" } });
  
//     // Submit the form
//     fireEvent.click(getByText("Log In"));

//     // Assert that the loading indicator or success message is displayed
//     expect(getByTestId("loading-indicator")).toBeInTheDocument();
//   });
});
