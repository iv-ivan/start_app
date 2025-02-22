import { Header } from "./header";
import { Footer } from "./footer";
import { InputField } from "./input_field";

export function Main() {
  return (
      <div className="flex flex-col h-screen">
        <Header />
        <InputField />
        <Footer />
      </div>
  );
}
