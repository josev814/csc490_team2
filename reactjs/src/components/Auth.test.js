import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import App from '../App';

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
    // const loginLink = screen.getByText(/Login/i);
    // fireEvent.click(loginLink);
    
    const form = screen.getByRole('form')
    const registerLink = within(form).getByRole('link', {name: /Register/i})
    
    fireEvent.click(registerLink);

    expect(screen.getByText("Account Registration")).toBeInTheDocument();
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  // test("switches back to login form when 'Log In' link is clicked", () => {
  //   const { getByText, getByLabelText } = render(<LoginRegister />);
  //   const registerLink = getByText("Register");
  //   fireEvent.click(registerLink);

  //   const loginLink = getByText("Log In");
  //   fireEvent.click(loginLink);

  //   expect(getByText("Account Login")).toBeInTheDocument();
  //   expect(getByText("Register")).toBeInTheDocument();
  //   expect(getByLabelText("Email address")).toBeInTheDocument();
  //   expect(getByLabelText("Password")).toBeInTheDocument();
  // });

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

//   test("displays error message on login form submission failure", () => {
//     const { getByLabelText, getByText, getByTestId } = render(<LoginRegister />);
  
//     // Fill in the form fields with invalid data
//     fireEvent.change(getByLabelText("Email address"), { target: { value: "invalid-email" } });
//     fireEvent.change(getByLabelText("Password"), { target: { value: "" } });
  
//     // Submit the form
//     fireEvent.click(getByText("Log In"));

//     // Assert that the error message is displayed
//     expect(getByTestId("error-message")).toBeInTheDocument();
//   });

//   test("prevents login form submission with invalid input", () => {
//     const { getByLabelText, getByText, queryByTestId } = render(<LoginRegister />);
  
//     // Fill in the form fields with invalid data
//     fireEvent.change(getByLabelText("Email address"), { target: { value: "invalid-email" } });
//     fireEvent.change(getByLabelText("Password"), { target: { value: "" } });
  
//     // Try to submit the form
//     fireEvent.click(getByText("Log In"));

//     // Assert that the loading indicator or success message is not displayed
//     expect(queryByTestId("loading-indicator")).toBeNull();
//   });
});
