import Cookies from 'universal-cookie';
import axios from 'axios';

const cookies = new Cookies(null, { path: '/' });

export const sitedetails = {
    sitename: 'Stock Strategies',
    tagline: 'Test Trading Strategies',
    django_url: 'http://localhost:8889',
};

export function get_auth_header() {
    const token = localStorage.getItem('accessToken');
    const headers = {
        Authorization: `Bearer ${token}`,
    };
    return headers;
}

  export function refresh_login_cookie() {
    let currentPath = window.location.pathname;
    if (!currentPath.endsWith('/')){
        currentPath += '/'
    }

    //const navigation = useNavigate();
    if (['/', '/login/', '/register/'].includes(currentPath)) {
        return false
    }
    // Calculate expiration time for the login status cookie (30 minutes)
    const loginStatusExpiration = new Date();
    loginStatusExpiration.setTime(loginStatusExpiration.getTime() + (0.5 * 60 * 60 * 1000));

    // Check if 'is_active' cookie exists
    const is_active = cookies.get('is_active');
    if (is_active) {
        // Log the current value of 'is_active' (optional for debugging)

        // Update the expiration time of the 'is_active' cookie
        cookies.set('is_active', is_active, { expires: loginStatusExpiration });
        return true
    } else {
        console.error("User is not logged in.");
        window.location.assign('/login');
    }
    return false
}

export async function refresh_token() {
    const refresh_url = `${sitedetails.django_url}/auth/refresh/`;
    const data = {'refresh': localStorage.getItem('refreshToken')};
    if(data['refresh'] === undefined){
        return
    }
    try {
        // Send POST request to refresh URL
        const response = await axios.post(refresh_url, data, { headers: get_auth_header() });

        // Check if response is successful
        if (response.status === 200) {
            // Update tokens in local storage
            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('refreshToken', response.data.refresh);
        } else {
            // Handle unexpected response status codes
            // TODO: toastify this
            console.error('Error refreshing token')
            console.error('Unexpected response status:', response.status);
        }
    } catch (error) {
        // Handle network errors or other exceptions
        // TODO: toastify this
        console.error('Error refreshing token:', error);
        // Optionally, navigate to login page or handle the error
    }
}

export async function refresh_session(){
    if (sitedetails.django_url === undefined){
        return
    }
    let user_url = get_user_from_cookie()
    if(user_url !== undefined){
        if (refresh_login_cookie()){
            refresh_token()
        }
    }
    console.groupEnd()
}

export function get_user_from_cookie() {
    const userCookie = cookies.get('user');
    if (!userCookie || !userCookie.id) {
        console.error("User cookie or user ID not found.");
        return null; // or handle the error appropriately
    }

    // Construct user URL based on user ID
    const user_id = userCookie.id;
    const user_url = `${sitedetails.django_url}/users/${user_id}/`;
    return user_url;
}