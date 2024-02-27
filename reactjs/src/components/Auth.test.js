import React from "react";
import { render, waitFor, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event"; // Importing userEvent

import AuthForm from "./Auth"; // Assuming the original file is named "auth.js"

describe("AuthForm component", () => {
  test("renders login form by default", () => {
    render(<AuthForm />);
    
    expect(screen.getByText("Account Login")).toBeInTheDocument();
    expect(screen.getByText("Register")).toBeInTheDocument();
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  test("switches to registration form when 'Register' link is clicked", async () => {
    render(<AuthForm />);
    const registerLink = screen.getByText("Register");

    userEvent.click(registerLink); // Using userEvent to simulate a click event

    await waitFor(() => {
      expect(screen.getByText("Account Registration")).toBeInTheDocument();
      expect(screen.getByText("Log In")).toBeInTheDocument();
      expect(screen.getByLabelText("Email address")).toBeInTheDocument();
      expect(screen.getByLabelText("Password")).toBeInTheDocument();
    });
  });

  test("switches back to login form when 'Log In' link is clicked", async () => {
    render(<AuthForm />);
    const registerLink = screen.getByText("Register");
    userEvent.click(registerLink); // Switch to registration form

    const loginLink = screen.getByText("Log In");
    userEvent.click(loginLink); // Switch back to login form

    await waitFor(() => {
      expect(screen.getByText("Account Login")).toBeInTheDocument();
      expect(screen.getByText("Register")).toBeInTheDocument();
      expect(screen.getByLabelText("Email address")).toBeInTheDocument();
      expect(screen.getByLabelText("Password")).toBeInTheDocument();
    });
  });

  // Add more tests for form submission, error handling, etc.
});
