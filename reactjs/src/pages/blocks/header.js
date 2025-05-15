
export default function Header(){
    return (
        <header className="col-12 bg-dark flex-md-nowrap p-3">
            <h1 className="text-white">{global.config.sitedetails.sitename}</h1>
            <h4 className="text-white">{global.config.sitedetails.tagline}</h4>
        </header>
    )
}
