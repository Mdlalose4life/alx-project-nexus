import Image from "next/image"

const HeroSection: React.FC = () => {
    return (
        <section className="">
            <div className="max-w-ful">
                <Image 
                src="/Images/Hero.png"
                alt="Hero"
                height={700}
                width={1800}
                className="rounded-lg p-1" />
            </div>
        </section>
    )
}
export default HeroSection