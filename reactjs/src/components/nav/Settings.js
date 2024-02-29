
export default function Home(){
    return (
        <div classNameName="wrapper bg-white mt-sm-5">
    <h4 className="pb-4 border-bottom">Account settings</h4>
    <div className="py-2">
        <div className="row py-2">
            <div className="col-md-6">
                <label for="firstname">First Name</label>
                <input type="text" className="bg-light form-control" placeholder="Enter First name.."/>
            </div>
            <div className="col-md-6 pt-md-0 pt-3">
                <label for="lastname">Last Name</label>
                <input type="text" className="bg-light form-control" placeholder="Enter Last Name..."/>
            </div>
        </div>
        <div className="row py-2">
            <div className="col-md-6">
                <label for="email">Email Address</label>
                <input type="text" className="bg-light form-control" placeholder="Enter Email Address..."/>
            </div>
            <div className="col-md-6 pt-md-0 pt-3">
                <label for="phone">Phone Number</label>
                <input type="tel" className="bg-light form-control" placeholder="Enter Phone Number..."/>
            </div>
        </div>
        <div className="mx-auto py-3 pb-4 border-bottom">
            <button className="btn btn-primary mr-3">Save Changes</button>
            <button className="btn border button">Cancel</button>
        </div>
        <div className="d-sm-flex align-items-center pt-3" id="deactivate">
            <div>
                <b>Deactivate your account</b>
                <p>Details about your account and password will be erased!</p>
            </div>
            <div className="ml-10">
                <button className="btn danger">Deactivate</button>
            </div>
        </div>
    </div>
</div>
    );
};