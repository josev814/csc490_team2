import TeamCards from '../components/cards/people';
import { Link } from 'react-router-dom';

export default function Home(){
    return (
        <>
        <div className='row pretty-background vh-100 m-0'>
            <div className='col-md-6 d-flex justify-content-center align-items-center h-100'>
                <div className='d-flex align-items-center h-100 w-75'>
                    <div>
                        <h2 className='fs-1'>Test Your Trading Strategies</h2>
                        <h4 className='fs-3'>Mock Trading with Realtime Stock data</h4>
                        <h4 className='fs-3'>
                            Create Test Trading strategies against the market
                        </h4>
                        <p className='fs-5'>
                            Our platform allows you to run test strategies against a stocks history and it&apos;s ongoing market value.
                            Create as many strategies against any stock that you like.
                            Once you find a strategy that works for you implement it on your own trading service like E-Trade.
                        </p>
                        <Link to='/register'>
                            <button className='bg-warning btn btn-lg'>Start Now</button>
                        </Link>
                    </div>
                </div>
            </div>
            <div className='col-md-6 d-flex justify-content-end align-items-center h-100 p-0 overflow-hidden'>
                <img src='/images/ui-screenshot.png' alt='UI Screenshot' className='img-fluid shadow-sm mb-5 rounded-start' />
            </div>
        </div>
        <div className='container-fluid'>
            <div className='d-flex justify-content-center'>
                <div className='row p-5'>
                    <span className='pb-3'>Developed by Seniors at</span>
                    <img src='/images/FSULogo.svg' alt='Fayetteville State University Logo' />
                </div>
            </div>
        </div>
        <div className="container-fluid bg-meet p-3">
            <div className='d-flex justify-content-center pb-3'>
                <h3>Meet the Team</h3>
            </div>
            <div className='row d-flex justify-content-center gap-5'>
                <TeamCards img='dr-mingxian-jin-150.png' name="Dr. Mingxian Jin " position='Advisor' linkedin='mingxian-jin-3a135024' />
                <TeamCards img='jose-vargas-150.png' name="Jose' Vargas" position='Team Lead' linkedin='josevargas814' />
                <TeamCards img='caileb-carter-150.png' name="Caileb Carter" position='Lead Frontend Developer' linkedin='caileb-carter-940150180' />
                <TeamCards img='stathis-jones-150.png' name="Stathis Jones" position='Lead Backend Developer' linkedin='stathis-jones-a69973271' />
            </div>
        </div>
        </>
    );
};
