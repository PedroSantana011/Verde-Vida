from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.anchorlayout import AnchorLayout

# Configuração do tamanho da janela
Window.size = (360, 640)

class VerdeVidaApp(App):
    def build(self):
        self.cart_items = []  # Lista para armazenar os itens no carrinho
        self.screen_manager = ScreenManager()

        # Tela principal
        main_screen = Screen(name="main")
        main_screen.add_widget(self.build_main_screen())
        self.screen_manager.add_widget(main_screen)

        # Tela de checkout
        checkout_screen = Screen(name="checkout")
        checkout_screen.add_widget(self.build_checkout_screen())
        self.screen_manager.add_widget(checkout_screen)

        return self.screen_manager

    def build_main_screen(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título
        title = Label(
            text="VERDEVIDA FAZENDA URBANA",
            font_size=26,
            color=(0, 0.5, 0, 1),
            size_hint_y=None,
            height=50,
            valign='middle',
            halign='center',
            text_size=(Window.width, 50)
        )
        root.add_widget(title)

        # ScrollView com lista de produtos
        product_list = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-120))
        layout = GridLayout(cols=1, size_hint_y=None, spacing=15, padding=[10, 10])
        layout.bind(minimum_height=layout.setter('height'))

        # Adicionando produtos
        layout.add_widget(self.create_product("ALFACE", "Produto fresco e saudável.\nCultivado em sistema hidropônico.", "R$ 2,50 / unidade", 2.50))
        layout.add_widget(self.create_product("TOMATE", "Rico em antioxidantes.\nIdeal para saladas e molhos.", "R$ 4,00 / quilo", 4.00))
        layout.add_widget(self.create_product("HORTELÃ", "Erva aromática perfeita\npara chás e temperos.", "R$ 2,00 / maço", 2.00))

        # Adicionando a lista de produtos ao ScrollView
        product_list.add_widget(layout)
        root.add_widget(product_list)

        # Botão do carrinho de compras
        cart_button = Button(text="Carrinho de Compras", size_hint=(1, None), height=50, background_normal='', background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        cart_button.bind(on_press=self.show_cart_popup)  # Chama o popup do carrinho
        root.add_widget(cart_button)

        return root

    def create_product(self, name, description, price_text, price_value):
        # Layout de cada produto
        product_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=170, padding=15, spacing=10)

        # Nome do produto
        name_label = Label(text=name, font_size=20, color=(0, 0.4, 0, 1))
        product_layout.add_widget(name_label)

        # Descrição do produto
        description_label = Label(text=description, font_size=14, color=(0.2, 0.2, 0.2, 1))
        product_layout.add_widget(description_label)

        # Preço do produto
        price_label = Label(text=price_text, font_size=16, color=(0, 0.5, 0, 1))
        product_layout.add_widget(price_label)

        # Botão para abrir o popup de quantidade
        buy_button = Button(text="Selecionar Quantidade", size_hint=(1, None), height=40, background_normal='', background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=16)
        buy_button.bind(on_press=lambda instance, name=name, price=price_value: self.show_quantity_popup(name, price))
        product_layout.add_widget(buy_button)

        return product_layout

    def show_quantity_popup(self, product_name, price):
        # Layout do Popup
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Texto para indicar o nome do produto
        product_label = Label(text=f"Quantos {product_name} deseja?", font_size=20, color=(0, 0.5, 0, 1))
        popup_layout.add_widget(product_label)

        # Slider para selecionar a quantidade
        quantity_slider = Slider(min=1, max=10, value=1, step=1, size_hint_y=None, height=50)
        popup_layout.add_widget(quantity_slider)

        # Texto para mostrar a quantidade selecionada
        quantity_label = Label(text=f"Quantidade: {int(quantity_slider.value)}", font_size=18, color=(0, 0.5, 0, 1), size_hint_y=None, height=40)
        popup_layout.add_widget(quantity_label)

        # Texto para mostrar o valor total
        total_label = Label(text=f"Valor Total: R$ {price:.2f}", font_size=18, color=(0, 0.5, 0, 1), size_hint_y=None, height=40)
        popup_layout.add_widget(total_label)

        # Função para atualizar o valor total ao mudar a quantidade
        def update_total(instance, value):
            quantity_label.text = f"Quantidade: {int(value)}"
            total_label.text = f"Valor Total: R$ {value * price:.2f}"

        quantity_slider.bind(value=update_total)

        # Botão para adicionar ao carrinho
        add_button = Button(text="Adicionar ao Carrinho", size_hint_y=None, height=50, background_normal='', background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        add_button.bind(on_press=lambda instance: self.add_to_cart(product_name, quantity_slider.value, price, popup))
        popup_layout.add_widget(add_button)

        # Botão para fechar o popup
        close_button = Button(text="Fechar", size_hint_y=None, height=40, background_normal='', background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1), font_size=18)
        close_button.bind(on_press=lambda instance: popup.dismiss())
        popup_layout.add_widget(close_button)

        # Criar e exibir o popup
        popup = Popup(title=f"{product_name}", content=popup_layout, size_hint=(0.85, 0.65))
        popup.open()

    def add_to_cart(self, product_name, quantity, price, popup):
        quantity = int(quantity)
        if quantity > 0:
            self.cart_items.append((product_name, quantity, price * quantity))  # Adiciona o produto ao carrinho
            popup.dismiss()  # Fecha o popup após adicionar ao carrinho

    def show_cart_popup(self, instance):
        # Layout do Popup do Carrinho
        cart_popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Cabeçalho do carrinho
        cart_label = Label(text="Carrinho de Compras", font_size=24, color=(0, 0.5, 0, 1))
        cart_popup_layout.add_widget(cart_label)

        # Exibindo os itens no carrinho
        total_value = 0
        if not self.cart_items:
            empty_label = Label(text="Carrinho vazio.", font_size=18, color=(1, 0, 0, 1))
            cart_popup_layout.add_widget(empty_label)
        else:
            for item in self.cart_items:
                product_name, quantity, total = item
                item_label = Label(text=f"{product_name} - {quantity} unidades - R$ {total:.2f}", font_size=16, color=(0, 0.5, 0, 1))
                cart_popup_layout.add_widget(item_label)
                total_value += total

        # Exibindo o valor total
        total_cart_label = Label(text=f"Valor Total do Carrinho: R$ {total_value:.2f}", font_size=18, color=(0, 0.5, 0, 1), size_hint_y=None, height=40)
        cart_popup_layout.add_widget(total_cart_label)

        # Botão para finalizar o pedido
        finalize_button = Button(text="Finalizar Pedido", size_hint_y=None, height=50, background_normal='', background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=18)
        finalize_button.bind(on_press=lambda instance: self.finalize_order(cart_popup))
        cart_popup_layout.add_widget(finalize_button)

        # Botão para esvaziar o carrinho
        clear_button = Button(text="Esvaziar Carrinho", size_hint_y=None, height=40, background_normal='', background_color=(1, 0, 0, 1), color=(1, 1, 1, 1), font_size=18)
        clear_button.bind(on_press=lambda instance: self.clear_cart(cart_popup))
        cart_popup_layout.add_widget(clear_button)

        # Botão para fechar o carrinho
        close_button = Button(text="Fechar", size_hint_y=None, height=40, background_normal='', background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1), font_size=18)
        close_button.bind(on_press=lambda instance: cart_popup.dismiss())
        cart_popup_layout.add_widget(close_button)

        # Criar e exibir o popup
        cart_popup = Popup(title="Carrinho", content=cart_popup_layout, size_hint=(0.85, 0.7))
        cart_popup.open()

    def finalize_order(self, cart_popup):
        if self.cart_items:
            self.screen_manager.current = "checkout"  # Muda para a tela de checkout
            cart_popup.dismiss()  # Fecha o popup

    def clear_cart(self, cart_popup):
        self.cart_items.clear()  # Esvaziar o carrinho
        cart_popup.dismiss()  # Fecha o popup
        self.show_cart_popup(None)  # Reabre o carrinho vazio

    def show_confirmation_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        thank_you_label = Label(
            text="Obrigado por comprar conosco!\n\nO recibo da compra foi enviado para seu e-mail!",
            font_size=20,
            color=(0, 0.5, 0, 1),
            halign='center',
            valign='middle',
            text_size=(300, None)
        )
        popup_layout.add_widget(thank_you_label)

        def return_to_home(instance):
            self.cart_items.clear()  # Esvaziar o carrinho
            self.screen_manager.current = "main"  # Retornar para a tela inicial
            confirmation_popup.dismiss()  # Fecha completamente o popup

        # Botão para fechar o popup e voltar à tela inicial
        close_button = Button(
            text="Fechar",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0, 0.5, 0, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        close_button.bind(on_press=return_to_home)
        popup_layout.add_widget(close_button)

        confirmation_popup = Popup(
            title="Pedido Confirmado",
            content=popup_layout,
            size_hint=(0.85, 0.5)
        )
        confirmation_popup.open()

    def build_checkout_screen(self):
        root = BoxLayout(orientation='vertical')
        checkout_layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=15,
            size_hint=(None, None),
            width=300
        )
        checkout_layout.bind(minimum_height=checkout_layout.setter('height'))

        title = Label(
            text="Informações de Compra",
            font_size=26,
            color=(0, 0.5, 0, 1),
            size_hint_y=None,
            height=50,
            halign='center',
            valign='middle',
            text_size=(300, 50)
        )
        checkout_layout.add_widget(title)

        fields = ['Nome Completo', 'Endereço de Entrega', 'Telefone', 'Email']
        for field in fields:
            input_field = TextInput(
                hint_text=field,
                size_hint=(None, None),
                size=(280, 50),
                pos_hint={'center_x': 0.5},
                multiline=False,
                background_color=(1, 1, 1, 1),
                foreground_color=(0, 0.5, 0, 1),
                font_size=16
            )
            checkout_layout.add_widget(input_field)

        delivery_toggle = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            height=50,
            width=280,
            spacing=10,
            pos_hint={'center_x': 0.5}
        )
        delivery_button = ToggleButton(text='Entrega', group='delivery', size_hint_x=0.5, background_normal='', background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=16)
        pickup_button = ToggleButton(text='Retirada Presencial', group='delivery', size_hint_x=0.5, background_normal='', background_color=(0, 0.5, 0, 1), color=(1, 1, 1, 1), font_size=16)
        delivery_toggle.add_widget(delivery_button)
        delivery_toggle.add_widget(pickup_button)
        checkout_layout.add_widget(delivery_toggle)

        payment_info = Label(
            text="O pagamento deverá ser feito via PIX na entrega/retirada",
            font_size=16,
            color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(280, 40),
            halign='center',
            valign='middle',
            text_size=(280, 40),
            pos_hint={'center_x': 0.5}
        )
        checkout_layout.add_widget(payment_info)

        confirm_button = Button(
            text="Confirmar Pedido",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0, 0.5, 0, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        confirm_button.bind(on_press=self.show_confirmation_popup)
        checkout_layout.add_widget(confirm_button)

        anchor_layout = AnchorLayout()
        anchor_layout.add_widget(checkout_layout)
        root.add_widget(anchor_layout)

        return root

if __name__ == "__main__":
    VerdeVidaApp().run()