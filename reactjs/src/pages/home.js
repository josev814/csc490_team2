import TeamCards from '../components/cards/people';

export default function Home(){
    return (
        <>
        <h1>Home</h1>
        <div>
            Mock Trading with Realtime Stock data
        </div>
        <div className="container-fluid bg-info p-3">
            <div className='d-flex justify-content-center'>
                <h3>Meet the Team</h3>
            </div>
            <div className='row d-flex justify-content-center gap-5'>
                <TeamCards img='jose-vargas-150.png' name="Jose' Vargas" position='Team Lead' linkedin='josevargas814' />
                <TeamCards img='caileb-carter.jpg' name="Caileb Carter" position='Lead Frontend Developer' linkedin='caileb-carter-940150180' />
                <TeamCards img='stathis-jones.jpg' name="Stathis Jones" position='Lead Backend Developer' linkedin='stathis-jones-a69973271' />
            </div>
        </div>
        </>
    );
};
