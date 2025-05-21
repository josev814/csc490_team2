import '@testing-library/jest-dom';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import { RouterProvider } from 'react-router';
import { createMemoryRouter } from 'react-router-dom';
import getRoutes from '../Routes';
import { sitedetails, get_auth_header, get_user_from_cookie, refresh_session } from '../utils/appContext';

// suppressing v7 transition messages
beforeAll(() => {
  jest.spyOn(console, 'warn').mockImplementation((msg) => {
    if (
      typeof msg === 'string' &&
      msg.includes('React Router Future Flag Warning')
    ) return;
    console.warn(msg);
  });
});

const renderWithRoute = async (route: string) => {
  const testRouter = createMemoryRouter(
    getRoutes({
      sitedetails,
      get_auth_header,
      get_user_from_cookie,
      refresh_session,
    }),
     {
    initialEntries: [route],
  })
  render(
    <RouterProvider router={testRouter} />
  );
  await waitFor(() => {
    expect(screen.getByTestId('site-footer')).toBeInTheDocument();
  }, { timeout: 5000 });
};

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

  test("test invalid email login form submission failure", async () => {
    await renderWithRoute('/login');

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
    await renderWithRoute('/login');
    const form = screen.getByRole('form')
    
  
    fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123" } });
    fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "" } });

    // Submit the form
    fireEvent.click(within(form).getByText("Login"));
    
    // Assert that the error message is displayed
    expect(await screen.findByText(/Invalid Credentials/i)).toBeInTheDocument();
  });

  test("test short password login form submission failure", async () => {
    await renderWithRoute('/login');
    const form = screen.getByRole('form')
  
    fireEvent.change(within(form).getByLabelText("Email address"), { target: { value: "test@abc123" } });
    fireEvent.change(within(form).getByLabelText("Password"), { target: { value: "asdf" } });

    // Submit the form
    fireEvent.click(within(form).getByText("Login"));  
    
    // Assert that the error message is displayed
    expect(await screen.findByText(/Invalid Credentials/i)).toBeInTheDocument();
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
