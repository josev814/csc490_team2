import { RouteObject } from 'react-router';
import { LoginRegister, Logout } from './components/Auth';
import AuthedLayout from './pages/authedlayout';
import UnauthedLayout from './pages/unauthedlayout';
import NoPage from './pages/nopage';
import Home from './pages/home';
import FIND_STOCK from './pages/stocks';
import SHOW_TICKER from './pages/show_ticker';
import SHOW_TICKER_NEWS from './pages/news';
import LIST_RULES from './pages/rules';
import Settings from './components/nav/Settings'
import { SHOW_RULE, CREATE_RULE } from './pages/rule';
import EditRuleForm from './components/rules/EditRule';

type SiteDetails = {
    sitename: string;
    tagline: string;
    django_url: string;
};

export default function getRoutes(
    {sitedetails, get_auth_header, get_user_from_cookie, refresh_session}: {
        sitedetails: SiteDetails;
        get_auth_header: () => object;
        get_user_from_cookie: () => string | null;
        refresh_session: () => void;
    }): RouteObject [] {
        return [
            {
                path: '/',
                element: (
                <UnauthedLayout
                    sitename={sitedetails.sitename}
                    tagline={sitedetails.tagline}
                />
                ),
                children: [
                { index: true, element: <Home /> },
                { path: 'login', element: <LoginRegister mode="signin" /> },
                { path: 'register', element: <LoginRegister mode="signup" /> },
                { path: 'logout', element: <Logout /> },
                ],
            },{
                path: '/user/',
                element: (
                <AuthedLayout
                    sitename={sitedetails.sitename}
                    tagline={sitedetails.tagline}
                    refresh_session={refresh_session}
                />
                ),
                children: [
                { path: ':user_id/profile', element: <> </> },
                { path: ":user_id/settings", element: (<Settings />)}
                ],
            },{
                path: '/stocks/',
                element: (
                <AuthedLayout
                    sitename={sitedetails.sitename}
                    tagline={sitedetails.tagline}
                />
                ),
                children: [
                { index: true, element: <FIND_STOCK /> },
                { path: ':ticker', element: <SHOW_TICKER /> },
                { path: ':ticker/news', element: <SHOW_TICKER_NEWS /> }
                ],
            },{
                path: '/rules/',
                element: (
                <AuthedLayout
                    sitename={sitedetails.sitename}
                    tagline={sitedetails.tagline}
                    django_url={sitedetails.django_url}
                />
                ),
                children: [
                { index: true, element: <LIST_RULES get_auth_header={get_auth_header} django_url={sitedetails.django_url} /> }
                ]
            },{
                path: '/rule/',
                element: (
                <AuthedLayout
                    sitename={sitedetails.sitename}
                    tagline={sitedetails.tagline}
                    django_url={sitedetails.django_url}
                />
                ),
                children: [
                { path: 'create', element: <CREATE_RULE django_url={sitedetails.django_url} get_auth_header={get_auth_header} get_user_from_cookie={get_user_from_cookie} />},
                { path: ':rule/:rule_name', element: <SHOW_RULE sitedetails={sitedetails} get_auth_header={get_auth_header} />},
                { path: ':rule/:rule_name/edit', element: <EditRuleForm sitedetails={sitedetails} get_auth_header={get_auth_header} />},
                
                ]
            },{
                path: '*',
                element: (
                <UnauthedLayout
                    sitename={sitedetails.sitename}
                    tagline={sitedetails.tagline}
                />
                ),
                children: [
                { index: true, element: <NoPage />},
                { path: '*', element: <NoPage />},
                ]
            }
        ];
    }
