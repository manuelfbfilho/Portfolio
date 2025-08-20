import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_curve, auc, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# ----------------------------------------------------
# 1. Preparação e Modelagem dos Dados (Lógica Separada)
# ----------------------------------------------------

def load_and_prepare_data():
    """Carrega e pré-processa os dados."""
    try:
        df = pd.read_csv('./data/dados_tratados.csv')
    except FileNotFoundError:
        return None, None, None, None, None

    # Renomeando colunas e tratando dados
    df.rename(columns={'customer.gender': 'gender', 'customer.SeniorCitizen': 'seniorcitizen',
                       'customer.Partner': 'partner', 'customer.Dependents': 'dependents',
                       'customer.tenure': 'tenure', 'phone.PhoneService': 'phoneservice',
                       'phone.MultipleLines': 'multiplelines', 'internet.InternetService': 'internetservice',
                       'internet.OnlineSecurity': 'onlinesecurity', 'internet.OnlineBackup': 'onlinebackup',
                       'internet.DeviceProtection': 'deviceprotection', 'internet.TechSupport': 'techsupport',
                       'internet.StreamingTV': 'streamingtv', 'internet.StreamingMovies': 'streamingmovies',
                       'account.Contract': 'contract', 'account.PaperlessBilling': 'paperlessbilling',
                       'account.PaymentMethod': 'paymentmethod', 'account.Charges.Monthly': 'chargesmonthly',
                       'account.Charges.Total': 'chargestotal'}, inplace=True)
    
    # Adicionando correção para NaN na coluna `account.Charges.Total`
    df['chargestotal'] = pd.to_numeric(df['chargestotal'], errors='coerce')
    df.dropna(subset=['chargestotal'], inplace=True)
    
    # Removendo linhas com valores nulos na coluna 'Churn'
    df.dropna(subset=['Churn'], inplace=True)
    
    df['Churn'] = df['Churn'].map({'Evasão': 1, 'Ativo': 0})

    X = df.drop('Churn', axis=1)
    y = df['Churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    return df, X_train, X_test, y_train, y_test

def train_models(X_train, X_test, y_train, y_test):
    """Treina os modelos e retorna as métricas."""
    if X_train is None:
        return None, None, None, None, None, None, None, None
    
    numerical_features = X_train.select_dtypes(include=np.number).columns.tolist()
    categorical_features = X_train.select_dtypes(include='object').columns.tolist()
    categorical_features.remove('customerID')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # Modelos
    logreg_pipeline = Pipeline([('preprocessor', preprocessor), ('classifier', LogisticRegression(random_state=42))])
    rf_pipeline = Pipeline([('preprocessor', preprocessor), ('classifier', RandomForestClassifier(random_state=42))])

    logreg_pipeline.fit(X_train, y_train)
    rf_pipeline.fit(X_train, y_train)

    y_proba_logreg = logreg_pipeline.predict_proba(X_test)[:, 1]
    y_proba_rf = rf_pipeline.predict_proba(X_test)[:, 1]

    # Relatórios de classificação
    y_pred_rf = rf_pipeline.predict(X_test)
    report_rf = classification_report(y_test, y_pred_rf, target_names=['Ativo', 'Evasão'], output_dict=True)

    return logreg_pipeline, rf_pipeline, y_proba_logreg, y_proba_rf, report_rf, preprocessor, numerical_features, categorical_features

df, X_train, X_test, y_train, y_test = load_and_prepare_data()
logreg_pipeline, rf_pipeline, y_proba_logreg, y_proba_rf, report_rf, preprocessor, numerical_features, categorical_features = train_models(X_train, X_test, y_train, y_test)

# ----------------------------------------------------
# 2. Configuração do Dashboard Dash
# ----------------------------------------------------

app = dash.Dash(__name__)

# Funções para gerar gráficos Plotly
def create_roc_curve(y_test, y_proba_logreg, y_proba_rf):
    fpr_logreg, tpr_logreg, _ = roc_curve(y_test, y_proba_logreg)
    roc_auc_logreg = auc(fpr_logreg, tpr_logreg)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, y_proba_rf)
    roc_auc_rf = auc(fpr_rf, tpr_rf)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr_logreg, y=tpr_logreg, mode='lines', name=f'Regressão Logística (AUC = {roc_auc_logreg:.2f})'))
    fig.add_trace(go.Scatter(x=fpr_rf, y=tpr_rf, mode='lines', name=f'Random Forest (AUC = {roc_auc_rf:.2f})'))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Aleatório', line=dict(dash='dash', color='gray')))
    fig.update_layout(title='Curva ROC', xaxis_title='Taxa de Falso Positivo', yaxis_title='Taxa de Verdadeiro Positivo')
    return fig

# >>> FUNÇÃO CORRIGIDA AQUI <<<
def create_feature_importance_chart(rf_pipeline, preprocessor, numerical_features, categorical_features):
    feature_importances = rf_pipeline.named_steps['classifier'].feature_importances_
    
    # Obtém os nomes das features do preprocessor
    feature_names = preprocessor.get_feature_names_out().tolist()

    df_importances = pd.DataFrame({'feature': feature_names, 'importance': feature_importances})
    df_importances.sort_values('importance', ascending=False, inplace=True)

    fig = px.bar(df_importances.head(15), x='importance', y='feature', orientation='h',
                 title='Top 15 Variáveis mais Importantes (Random Forest)')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def create_churn_distribution_chart(df):
    churn_counts = df['Churn'].map({0: 'Ativo', 1: 'Evasão'}).value_counts().reset_index()
    churn_counts.columns = ['status', 'count']
    fig = px.pie(churn_counts, values='count', names='status', title='Distribuição de Clientes Ativos vs. Evasão')
    return fig

# Layout do Dashboard
app.layout = html.Div(children=[
    html.H1(children='Telecom X - Análise e Previsão de Churn', style={'textAlign': 'center'}),
    html.H3(children='Painel Interativo de Análise Preditiva', style={'textAlign': 'center'}),
    
    # Condicional para exibir conteúdo apenas se os dados forem carregados e o treinamento bem-sucedido
    html.Div(id='dashboard-content', children=[
        html.Div([
            html.H4('Relatório de Classificação (Random Forest)'),
            html.Pre(classification_report(y_test, rf_pipeline.predict(X_test), target_names=['Ativo', 'Evasão'])),
        ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'margin': '20px', 'borderRadius': '5px'}),
        
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(
                    id='churn-distribution',
                    figure=create_churn_distribution_chart(df)
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
            
            html.Div(children=[
                dcc.Graph(
                    id='feature-importance',
                    figure=create_feature_importance_chart(rf_pipeline, preprocessor, numerical_features, categorical_features)
                )
            ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
        ], style={'padding': '10px'}),
        
        html.Div(children=[
            dcc.Graph(
                id='roc-curve',
                figure=create_roc_curve(y_test, y_proba_logreg, y_proba_rf)
            )
        ], style={'padding': '10px'})
    ]) if df is not None and rf_pipeline is not None else html.Div([
        html.H2("Erro ao carregar ou processar os dados.", style={'color': 'red'}),
        html.P("Verifique se o arquivo 'dados_tratados.csv' existe e se ele não contém problemas de formatação. O script não pôde ser executado."),
    ], style={'textAlign': 'center', 'marginTop': '50px'})
])

if __name__ == '__main__':
    app.run(debug=True)