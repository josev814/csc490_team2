import '@testing-library/jest-dom';
import { screen, fireEvent, waitFor, within, render } from '@testing-library/react';
import type {createMemoryRouter} from 'react-router-dom';
import { renderWithRoute } from './utils/testRouter';

// function removeLoginErrors(){
//   // reset invalid creds element
//   const invalidCredentialsElement = screen.queryByText(/Invalid Credentials/i);
//   if (invalidCredentialsElement) {
//     document.getElementById('login_errors').remove()
//   }
// }

describe("LoginRegister component", () => {
  test("go to login form", async () => {
    await renderWithRoute('/');

    const links = await screen.findAllByRole('link')
    const loginLink = links.find((link) => {
      if (link && link.textContent){ 
        return link.textContent.match(/Login/i);
      }
    })
    if(!loginLink){
      throw new Error('Login link was not found')
    }
    fireEvent.click(loginLink);
    expect(await screen.getByText(/Account Login/i)).toBeInTheDocument()
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  test("switches to registration form when 'Register' link is clicked", async () => {
    await renderWithRoute('/');

    const links = await screen.findAllByRole('link')
    const registerLink = links.find((link) => {
      if (link && link.textContent){ 
        return link.textContent.match(/Register/i);
      }
    })
    if(!registerLink){
      throw new Error('Registration link was not found')
    }
    fireEvent.click(registerLink);
    expect(await screen.findByText(/Account Registration/i)).toBeInTheDocument()
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  test("switches back to login form when 'Log In' link is clicked", async () => {
    await renderWithRoute('/register');

    const links = await screen.findAllByRole('link')
    const loginLink = links.find((link) => 
      link?.textContent?.match(/Log in/i)
    );

    if(!loginLink){
      throw new Error('Login link was not found')
    }
    
    fireEvent.click(loginLink);

    expect(await screen.getByText(/Account Login/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Email address")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  describe('invalid login tests', () => {
    let router: ReturnType<typeof createMemoryRouter>;

    beforeEach(async() => {
      router = await renderWithRoute('/login');
    });

    test("invalid email", async () => {
      const form = screen.getByRole('form')
    
      // Fill in the form fields with invalid data
      fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "invalid-email@123" } });
      fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "abcdabcd" } });

      // Submit the form
      fireEvent.click(within(form).getByText("Login"));

      // Submit the form
      fireEvent.click(within(form).getByText("Login"));
      
      // failed login
      expect(router.state.location.pathname).toBe('/login');
    });

    test("missing password", async () => {
      const form = screen.getByRole('form')
      
    
      fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123" } });
      fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "" } });

      // Submit the form
      fireEvent.click(within(form).getByText("Login"));
      
      // failed login
      expect(router.state.location.pathname).toBe('/login');
    });

    test("short password", async () => {
      const form = screen.getByRole('form')
    
      fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123" } });
      fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "asdf" } });

      // Submit the form
      fireEvent.click(within(form).getByText("Login"));
      
      // failed login
      expect(router.state.location.pathname).toBe('/login');
    });

    test("bad creds", async () => {
      const form = screen.getByRole('form')
    
      fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123.com" } });
      fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "asdfasdfa" } });

      // Submit the form
      fireEvent.click(within(form).getByText("Login"));
      expect(router.state.location.pathname).toBe('/login');
      
      // Assert that the error message is displayed
      const alert = await screen.findByRole('alert', {}, { timeout: 5000});
      expect(alert).toHaveTextContent(/Invalid Credentials/i);
    });
  });

  // test("submits login form with correct data", async () => {
  //   await renderWithRoute('/login');
  //   const form = screen.getByRole('form')

  //   // Fill in the form fields
  //   fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@example.com" } });
  //   fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "password123" } });
  
  //   // Submit the form
  //   fireEvent.click(within(form).getByText("Login"));  

  //   // Assert that the loading indicator or success message is displayed
  //   expect(screen.getByTestId("loading-indicator")).toBeInTheDocument();
  // });
});
